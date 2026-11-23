import unittest
from src.aid_review.nightscout import (
    NightscoutReadOnly,
    normalize_entries,
    summarize_entries,
)
from src.aid_review.review import build_review


class TestNightscoutAdapter(unittest.TestCase):
    def test_sgv_normalization(self):
        rows = normalize_entries([
            {"_id": "test1", "type": "sgv", "sgv": 145, "date": 1795406400000},
        ])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["mg_dl"], 145)
        self.assertEqual(rows[0]["timestamp"].utcoffset().total_seconds(), 0)

    def test_non_sgv_ignored(self):
        self.assertEqual(normalize_entries([{"type": "mbg", "sgv": 120}]), [])

    def test_missing_timestamp_fails_closed(self):
        with self.assertRaises(ValueError):
            normalize_entries([{"type": "sgv", "sgv": 120}])

    def test_duplicate_source_id(self):
        rows = normalize_entries([
            {"_id":"a","type":"sgv","dateString":"2026-11-23T14:00:00+08:00","sgv":100},
            {"_id":"a","type":"sgv","dateString":"2026-11-23T14:00:00+08:00","sgv":100},
        ])
        self.assertEqual(len(rows), 1)

    def test_no_auto_dose_or_aid_causality(self):
        data = [{"type":"sgv","sgv":185,"dateString":"2026-11-23T14:00:00+08:00"}]
        result = build_review(summarize_entries(data), mode="unknown", pump_events_verified=False)
        self.assertFalse(result["automatic_pump_changes"])
        self.assertIsNone(result["parameter_values_proposed"])
        self.assertTrue(any("未驗證" in text for text in result["warnings"]))

    def test_https_only(self):
        with self.assertRaises(ValueError):
            NightscoutReadOnly("http://example.com","test")
        with self.assertRaises(ValueError):
            NightscoutReadOnly("https://user:secret@example.com","test")

    def test_token_required(self):
        with self.assertRaises(ValueError):
            NightscoutReadOnly("https://example.com","")


if __name__ == "__main__":
    unittest.main()
