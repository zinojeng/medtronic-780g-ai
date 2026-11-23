from datetime import datetime

def parse_time(text: str) -> datetime:
    if not isinstance(text, str):
        raise ValueError("timestamp must be an ISO 8601 string")
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timezone-aware timestamp required")
    return value

def validate_cgm(points: list[dict]) -> list[dict]:
    result = []
    seen = set()
    for x in points:
        if set(("timestamp", "mg_dl")) - x.keys():
            raise ValueError("missing timestamp or mg_dl")
        ts = parse_time(x["timestamp"])
        mg_dl = x["mg_dl"]
        if isinstance(mg_dl, bool) or not isinstance(mg_dl, (float, int)) or not 20 <= mg_dl <= 600:
            raise ValueError("invalid SG reading; do not silently clip")
        source_id = x.get("source_event_id", x["timestamp"])
        if source_id in seen:
            continue
        seen.add(source_id)
        result.append({"timestamp": ts, "mg_dl": float(mg_dl), "source_event_id": str(source_id)})
    return sorted(result, key=lambda x: x["timestamp"])
