from .schema import validate_cgm

def summarize_cgm(points: list[dict], expected_minutes: int = 5) -> dict:
    """Sample-based exploratory statistics, not certified clinical AGP."""
    if expected_minutes <= 0:
        raise ValueError("expected_minutes must be positive")
    rows = validate_cgm(points)
    if not rows:
        return {"status": "insufficient_data", "n": 0}
    start, end = rows[0]["timestamp"], rows[-1]["timestamp"]
    duration_min = (end-start).total_seconds()/60
    expected_n = int(duration_min/expected_minutes)+1
    n = len(rows)
    gl = [r["mg_dl"] for r in rows]
    max_gap = max(((b["timestamp"]-a["timestamp"]).total_seconds()/60 for a,b in zip(rows, rows[1:])), default=0)
    pct = lambda pred: round(sum(pred(x) for x in gl)/n*100, 1)
    return {
        "status": "descriptive_only", "n": n, "start": start.isoformat(), "end": end.isoformat(),
        "coverage_pct_estimate": round(min(100.0,n/expected_n*100),1),
        "largest_gap_minutes": round(max_gap,1), "mean_sg_mg_dl": round(sum(gl)/n,1),
        "tir_70_180_pct": pct(lambda x: 70<=x<=180),
        "tbr_below_70_pct": pct(lambda x: x<70),
        "tbr_below_54_pct": pct(lambda x: x<54),
        "tar_above_180_pct": pct(lambda x: x>180),
        "tar_above_250_pct": pct(lambda x: x>250),
    }
