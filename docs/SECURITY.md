# Security, Privacy and Clinical Safety

- **No automated dosing**: 不寫入胰島素幫浦、不修改設定、不輸出具體個人化調整值。
- **Read-only credentials**: CareLink Token/密碼不得放在 repo、CI log、聊天記錄、LINE、公開 Worker 或測試檔。
- **Protected PHI**: 真實病人資料應留在經授權、受控的醫療環境；GitHub 僅儲存合成資料。
- **Controlled access**: 服務僅限內網/安全隧道，最小權限、加密及審計。
- **Data freshness**: SG 與 pump events 可能有不同延遲；不能用作即時警報。
- **Clinical review**: 所有參數檢視需醫師核對完整資料、風險、警訊與裝置原廠指引。
- **Research governance**: 如納入病人資料、模型訓練或研究需確認同意範圍、IRB、資安及資料治理。
- **Prompt boundaries**: LLM 只解讀經驗證的結構化分析結果，不能覆蓋安全規則。
