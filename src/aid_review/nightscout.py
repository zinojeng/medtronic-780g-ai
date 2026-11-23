"""Read-only Nightscout import for Medtronic Guardian Monitor research workflows.

Nightscout entries are NOT a verified 780G pump event stream.
The access token is loaded from environment variables and never printed.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from .analytics import summarize_cgm
from .review import build_review
from .schema import validate_cgm


class NightscoutError(RuntimeError):
    pass


def _base_url(value: str) -> str:
    parts = urlsplit(value.strip())
    if parts.scheme != "https" or not parts.hostname:
        raise ValueError("A valid HTTPS NIGHTSCOUT_URL is required")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("Nightscout URL must not embed credentials, query or fragment")
    return value.rstrip("/")


def normalize_entries(entries: list[dict]) -> list[dict]:
    """Convert Nightscout SGV entries into the shared CGM schema.

    Do not infer meals, insulin delivery, or AID parameter changes from SGV.
    Bad data fails closed instead of silently fabricating measurements.
    """
    if not isinstance(entries, list):
        raise ValueError("Expected a list of Nightscout entries")
    points = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Malformed Nightscout entry")
        if entry.get("type", "sgv") != "sgv":
            continue
        when = entry.get("dateString")
        if when is None:
            raw_ms = entry.get("date")
            if isinstance(raw_ms, bool) or not isinstance(raw_ms, (int, float)):
                raise ValueError("SGV entry missing dateString/date")
            when = datetime.fromtimestamp(raw_ms / 1000, tz=timezone.utc).isoformat()
        points.append({
            "source_event_id": str(entry.get("_id") or f'{when}:{entry.get("sgv")}'),
            "timestamp": when,
            "mg_dl": entry.get("sgv"),
        })
    return validate_cgm(points)


def summarize_entries(entries: list[dict]) -> dict:
    points = normalize_entries(entries)
    summary = summarize_cgm([
        {
            "timestamp": row["timestamp"].isoformat(),
            "mg_dl": row["mg_dl"],
            "source_event_id": row["source_event_id"],
        }
        for row in points
    ])
    if points:
        last = points[-1]["timestamp"]
        age_min = (datetime.now(timezone.utc) - last.astimezone(timezone.utc)).total_seconds() / 60
        summary["newest_reading_age_minutes"] = round(age_min, 1)
        summary["last_sensor_timestamp"] = last.isoformat()
        summary["source"] = "nightscout"
    return summary


class NightscoutReadOnly:
    def __init__(self, base_url: str, read_token: str):
        self.base_url = _base_url(base_url)
        if not read_token or not read_token.strip():
            raise ValueError("NIGHTSCOUT_READ_TOKEN is required")
        self._token = read_token.strip()

    def _fetch(self, path: str, count: int) -> list[dict]:
        if not 1 <= count <= 576:
            raise ValueError("count must be 1..576")
        # Nightscout v1 accepts a scoped access token via query parameter.
        # Never log this request URL: it contains a credential.
        url = self.base_url + path + "?" + urlencode({"count": count, "token": self._token})
        request = Request(url, headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=15) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                raise NightscoutError("Response too large")
            data = json.loads(body)
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            # Do not include the failing URL, response body or credential.
            raise NightscoutError("Nightscout fetch failed; check server and read-only token locally") from None
        if not isinstance(data, list):
            raise NightscoutError("Unexpected Nightscout response: array required")
        return data

    def read_glucose(self, count: int = 288) -> list[dict]:
        return self._fetch("/api/v1/entries.json", count=count)

    def read_treatments(self, count: int = 288) -> list[dict]:
        return self._fetch("/api/v1/treatments.json", count=count)


def main() -> None:
    """Minimal local preview. No raw identifiers, events or token are printed."""
    client = NightscoutReadOnly(
        os.environ.get("NIGHTSCOUT_URL", ""),
        os.environ.get("NIGHTSCOUT_READ_TOKEN", ""),
    )
    entries = client.read_glucose()
    summary = summarize_entries(entries)
    review = build_review(summary, mode="unknown", pump_events_verified=False)
    print(json.dumps({"cgm_summary": summary, "review": review}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
