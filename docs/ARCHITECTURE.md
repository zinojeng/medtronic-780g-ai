# Architecture / 系統架構

## 目標
讓 Medtronic MiniMed 780G 與先前 Libre AI 共用資料模型與分析邏輯，提供醫師審核的研究型 AID 決策支援，並可在充分驗證後整合既有 LINE Bot。

```text
MiniMed 780G -> MiniMed Mobile -> CareLink Patient
                                        |
                 [Read-only adapter; isolated credentials]
                                        |
                    Raw -> Validated -> Normalized events
                                        |
Libre CGM -> Libre adapter -------------+
                                        |
                       CGM quality / AID event analytics
                                        |
                    Clinician-review evidence cards
                                        |
                    Human approval and audit log
                                        |
                 LINE summary / research dashboard
```

## 資料層
1. **Raw**：僅在受控、加密環境保留原始匯出資料；不可提交 GitHub。
2. **Normalized**：source、deidentified_subject_id、source_event_id、event_time、ingest_time、data freshness、glucose、bolus、basal、carbs、SmartGuard mode；不完整欄位標示 unknown。
3. **Derived**：描述性 CGM 指標、餐食候選事件、pump delivery summaries、設定版本與前後比較。

## 分析規則
- CGM 上升不等於確認用餐；輸出候選時間與不確定性。
- Auto Basal 不得以 Manual basal profile 取代。
- ISF、ICR、AIT、SmartGuard target 要依使用模式分開說明。
- 完整 pump event 未同步時，僅能產出 CGM 描述性分析。
- 所有參數檢視卡必須標示資料來源、品質、替代解釋與審核者。

## LINE integration
沿用現有 LINE Messaging API；只傳送最少必要摘要、資料時間與安全連結；Webhook 不是主動推播端點。不得透過 LINE 傳送完整病人病歷或憑證。

## Safety
本專案不含 pump write API，不處理自動劑量變更，不取代原廠警報或治療決策。
