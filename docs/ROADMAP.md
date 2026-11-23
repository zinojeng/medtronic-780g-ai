# Roadmap / 開發看板

## Phase 0 — Offline MVP
- [x] 定義 read-only、clinician-review-only 安全界線
- [x] 合成資料、資料驗證、CGM 基礎指標與審查問題引擎
- [x] Python 單元測試與 GitHub Actions
- [x] 與 Libre / LINE 整合架構草案

## Phase 1 — CareLink 與 Libre 資料
- [x] Guardian Monitor → Nightscout 唯讀 SGV adapter / 單元測試（僅程式碼，未實測連線）
- [ ] 確認 App 已登入且 Nightscout 同步已啟用、取得自有站點網址
- [ ] 比對 Nightscout SGV 與 Guardian Monitor 真實資料新鮮度及缺漏
- [ ] 取得合法授權、去識別化的 CareLink 780G 匯出
- [ ] 比對 CSV 與 aidR / CareLink 官方報告
- [ ] 在受控環境測試 patient 登入、MFA、台灣地域相容性
- [ ] 統一 Libre CGM、CareLink CGM 的事件格式
- [ ] 完整記錄資料新鮮度、missingness、duplicate 與 provenance

## Phase 2 — AID analytics
- [ ] 餐食候選時間、carb / bolus timing 分析
- [ ] SmartGuard 自動校正與實際 basal delivery
- [ ] 模式退出、夜間與餐後血糖評估
- [ ] 設定變更版本與前後觀察性比較（考慮混雜與回歸均值）

## Phase 3 — Clinician-reviewed parameter assessment
- [ ] ICR、AIT、SmartGuard target、Manual Mode ISF 分類 evidence cards
- [ ] 資料品質門檻、不確定性、替代解釋與人工簽核
- [ ] 醫師審核記錄及修改後追蹤；初版不產生參數變更數值
- [ ] 臨床風險與安全審查後才評估更進階的研究模型

## Phase 4 — LINE + research
- [ ] 接入現有 LINE Bot 的定時 CGM / AID 回顧
- [ ] 研究用匯出與可稽核資料字典
- [ ] 效能、隱私、臨床一致性、安全閘門驗證

## Done 定義
每階段須有自動測試、對照資料與文件；不能以合成資料測試通過宣稱臨床可用。
