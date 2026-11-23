# CareLink Patient × MiniMed 780G 驗證計畫

## 優先順序
1. 在受控電腦由本人登入 CareLink Patient，匯出 7–14 天去識別化 CSV；不得將密碼與 Token 貼進聊天。
2. 比對官方 CareLink 報告，建立欄位字典及版本資訊。
3. 評估 [aidR](https://github.com/madleina/aidR) 解析歷史資料是否完整。
4. 另在測試環境評估 [carelink-python-client](https://github.com/ondrej1024/carelink-python-client) Patient 登入、台灣帳號、MFA 與讀取權限。
5. 若 API 不穩定，評估 [carelink-bridge](https://github.com/domien-f/carelink-bridge) 或 [nightscout-connect](https://github.com/nightscout/nightscout-connect)；不得繞過帳號安全機制。

## 驗收
- SG 數值、時間與單位對照；時區不得被重複轉換。
- Sensor timestamp 和 upload/ingest timestamp 分開。
- Bolus 類型、carb entries、SmartGuard/Manual mode、actual insulin delivery 可辨識且有事件來源。
- 離線/補傳/重複資料有明確處理，勿將舊數值冒充即時數值。
- 每日總胰島素、餐食 bolus、自動校正、模式使用率與官方報告逐項比對。
- 缺少完整 pump events 時標記未驗證，禁止推測 AID 因果作用。
- 先用合成資料；真實病人資料需適當授權、去識別化與資訊安全/倫理審查。

## 第一階段交付
可讀取受控範例 CSV 的 parser、schema 文件、品質報表及 golden-data 測試。尚無可確認的台灣 Patient 帳號自動登入結果。
