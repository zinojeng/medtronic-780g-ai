import json
import sys
from .analytics import summarize_cgm
from .review import build_review

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m src.aid_review.cli examples/synthetic_day.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    if not data.get("synthetic", False):
        raise SystemExit("MVP CLI accepts synthetic data only")
    metrics = summarize_cgm(data.get("cgm", []))
    print(json.dumps({"metrics":metrics, "review":build_review(metrics, mode=data.get("mode","unknown"))},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
