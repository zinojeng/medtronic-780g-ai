# Medtronic 780G × AI — Clinician-Reviewed AID Analytics (MVP)

> **Status:** Offline prototype using synthetic data only. Not connected to CareLink, Libre, LINE, or any insulin pump. **Never use this software to dose insulin or control an insulin pump.**

## 願景
整合 Medtronic MiniMed 780G / CareLink 與 Libre CGM 資料，分析 CGM 品質、血糖波動、SmartGuard 活動、餐食及胰島素事件，產生供醫師審核的參數檢視方向。**不自動修改幫浦設定、不生成個人化參數變更數值。**

## 780G 重點
- SmartGuard 相關設定包括 ICR、Active Insulin Time 與 SmartGuard glucose target。
- ISF/Manual Basal 的作用應區分 Manual Mode 與 SmartGuard，不能混為一談。
- 感測器血糖和完整 pump events 的更新速度可能不同。

## 快速開始（合成資料）
```bash
python3 -m unittest discover -s tests -v
python3 -m src.aid_review.cli examples/synthetic_day.json
```
需要 Python 3.10+；僅使用標準函式庫。

## 專案文件
- [架構](docs/ARCHITECTURE.md)
- [CareLink 資料驗證](docs/CARELINK_VALIDATION.md)
- [Roadmap](docs/ROADMAP.md)
- [安全與隱私](docs/SECURITY.md)

## 參考開源工具
- [carelink-python-client](https://github.com/ondrej1024/carelink-python-client)
- [carelink-bridge](https://github.com/domien-f/carelink-bridge)
- [nightscout-connect](https://github.com/nightscout/nightscout-connect)
- [aidR](https://github.com/madleina/aidR)

## 注意
本專案只支援研究與臨床決策支援，不負責即時低血糖警報或胰島素控制。禁止提交病人可識別資料、憑證或 Token。

## Guardian Monitor / Nightscout（實驗性唯讀串接）

Guardian Monitor App 的登入狀態**無法由這個 GitHub Repo 自動讀取**。若已在 App 啟用 Nightscout 同步，這裡可以透過 Nightscout API（read-only token）取得 SGV，作為 CGM 描述性分析輸入；尚未驗證真實 780G 帳號、bolus/AID 事件完整性，也無 pump-write 功能。

- [Guardian Monitor → Nightscout 設定及驗收](docs/GUARDIAN_MONITOR_SYNC.md)
- 核心模組：[`src/aid_review/nightscout.py`](src/aid_review/nightscout.py)
- 單元測試：[`tests/test_nightscout.py`](tests/test_nightscout.py)

本機自有安全 Nightscout 站點與 read-only access token 設好後：

```bash
export NIGHTSCOUT_URL='https://YOUR_PRIVATE_NIGHTSCOUT_HOST'
# 請在自己的裝置上安全設定 NIGHTSCOUT_READ_TOKEN，不要貼到聊天或 git
python3 -m src.aid_review.nightscout
```

**只印出摘要；不將真實 SG 或個人資料上傳 GitHub。**
