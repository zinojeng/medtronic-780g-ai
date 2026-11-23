import unittest
from src.aid_review.schema import validate_cgm
from src.aid_review.analytics import summarize_cgm
from src.aid_review.review import build_review

class TestSafety(unittest.TestCase):
    def test_tz_required(self):
        with self.assertRaises(ValueError):
            validate_cgm([{"timestamp":"2026-11-23T12:00:00","mg_dl":100}])

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            validate_cgm([{"timestamp":"2026-11-23T12:00:00+08:00","mg_dl":-1}])

    def test_dedupe(self):
        pts=[{"timestamp":"2026-11-23T12:00:00+08:00","mg_dl":100}]*2
        self.assertEqual(len(validate_cgm(pts)),1)

    def test_no_auto_dosing(self):
        points=[{"timestamp":f"2026-11-23T12:{i:02d}:00+08:00","mg_dl":200} for i in (0,5,10)]
        result=build_review(summarize_cgm(points),mode="smartguard")
        self.assertFalse(result["automatic_pump_changes"])
        self.assertIsNone(result["parameter_values_proposed"])
        self.assertIn("未驗證", " ".join(result["warnings"]))

    def test_insufficient_data(self):
        self.assertEqual(build_review(summarize_cgm([]))["decision"],"insufficient_data")

if __name__ == "__main__":
    unittest.main()
