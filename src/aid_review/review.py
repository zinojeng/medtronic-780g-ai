def build_review(s: dict, *, mode: str = "unknown", pump_events_verified: bool = False) -> dict:
    """Non-prescriptive review prompts. Never generates insulin setting values."""
    flags = []
    if s.get("status") != "descriptive_only":
        return {"decision":"insufficient_data","review_questions":[],"warnings":["沒有可供分析的血糖資料"]}
    if s["coverage_pct_estimate"] < 70 or s["largest_gap_minutes"] > 30:
        flags.append("資料覆蓋率或連續性不足：不得根據此摘要提出參數調整結論")
    if s["tbr_below_70_pct"] > 0:
        flags.append("資料中出現低血糖讀值，需人工核對裝置、症狀與事件")
    questions = [
        "確認此期間 SmartGuard / Manual Mode 與設定變更紀錄是否完整。",
        "若有反覆餐後高血糖，先比對碳水估算、餐前 bolus 時點及自動校正事件，再討論是否需要評估 ICR。",
        "比較 AIT 與 SmartGuard target 時，需審核低血糖風險及醫師所設定的個別治療目標。",
    ]
    if mode == "smartguard":
        questions.append("ISF 主要關聯 Manual Mode 校正；不要將 ISF 當成 SmartGuard 自動校正的主要可調參數。")
    if not pump_events_verified:
        flags.append("未驗證 bolus / basal / carb / mode events，不能將血糖趨勢歸因於特定 AID 動作")
    return {
        "decision": "clinician_review_only", "parameter_values_proposed": None,
        "automatic_pump_changes": False, "review_questions": questions, "warnings": flags
    }
