# 🌅 每日早安勵志圖自動發送系統

每天早上 7 點，自動將一張 AI 生成的精美勵志早安圖發送到你的 LINE！

**完全免費 · 無需伺服器 · 5 分鐘完成設定**

---

## 📸 效果預覽

```
┌─────────────────────────────────────────┐
│ 2026年03月17日  星期二         [左上角日期] │
│                                         │
│         🌅  早  安                      │
│   ─────────────────────────             │
│                                         │
│  「千里之行，始於足下。」               │
│                                         │
│       —— 老子  《道德經》               │
│                                         │
│  ✨ 每日早安 · 願你今天充滿能量 ✨      │
└─────────────────────────────────────────┘
        （背景為 Gemini AI 生成的晨景）
```

---

## 🗂️ 目錄結構

```
morning-image-bot/
├── .github/
│   └── workflows/
│       └── daily_morning.yml   ← GitHub Actions 排程
├── fonts/                      ← 字體目錄（Ubuntu 自動安裝）
├── main.py                     ← 主程式
├── quotes.py                   ← 50 則語錄資料庫
├── image_generator.py          ← 圖片生成模組
├── line_sender.py              ← LINE 推播模組
├── requirements.txt            ← Python 套件清單
└── README.md                   ← 本文件
```

---

## 🚀 快速開始（5 步驟）

### 第 1 步：Fork 本專案到你的 GitHub

1. 前往本專案的 GitHub 頁面
2. 點擊右上角 **Fork** 按鈕
3. 選擇你的帳號作為目標
4. 完成 Fork

---

### 第 2 步：取得 Google Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 帳號登入
3. 點擊 **「Create API Key」**
4. 選擇 **「Create API key in new project」**
5. 複製生成的 API Key（格式：`AIzaSy...`）

> **💡 費用說明：** Gemini Free Tier 每天提供 **50 次圖片生成**，完全免費。

---

### 第 3 步：設定 LINE Messaging API

#### 3a. 建立 LINE Bot

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 使用 LINE 帳號登入
3. 點擊 **「Create a new provider」**，輸入名稱（例：早安機器人）
4. 點擊 **「Create a Messaging API channel」**
5. 填寫必要資訊：
   - **Channel name**：早安勵志圖
   - **Channel description**：每日早安圖發送機器人
   - **Category**：個人
6. 同意條款，點擊 **「Create」**

#### 3b. 取得 Channel Access Token

1. 進入剛建立的 Channel
2. 點擊 **「Messaging API」** 標籤
3. 往下滑到 **「Channel access token」** 區塊
4. 點擊 **「Issue」** 生成 Token
5. 複製這串 Token（很長，開頭類似 `xxxxxxxxxxxx...`）

#### 3c. 取得你的 LINE User ID

**方法一（推薦）：** 使用 LINE Bot 取得

1. 在同一個 Messaging API 頁面，找到 **「Bot basic ID」**（格式：`@xxxxxxxx`）
2. 打開你的 LINE App，搜尋這個 ID 並加好友
3. 傳任一訊息給這個 Bot
4. 前往 [LINE Developers Console](https://developers.line.biz/console/) → 你的 Channel → **「Webhook」**
5. 啟用 Webhook，或查看 **「User ID」** 區塊

**方法二：** 使用 LINE API 查詢

```bash
# 在加好友後，Bot 會收到 follow event，從 webhook 的 source.userId 取得
# 或使用以下方式（將 TOKEN 換成你的 Channel Access Token）
curl -H "Authorization: Bearer TOKEN" https://api.line.me/v2/profile
```

> **⚠️ 注意：** User ID 格式為 `Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（U 開頭，32 碼）

#### 3d. 確認設定

1. 在 LINE Developers Console → Messaging API 標籤
2. 找到 **「Auto-reply messages」** → 設為 **Disabled**
3. 找到 **「Greeting messages」** → 可依喜好設定

---

### 第 4 步：取得 imgbb API Key（免費圖床）

1. 前往 [imgbb.com](https://imgbb.com/)
2. 點擊右上角 **「Sign up」** 免費註冊
3. 登入後，前往 [https://api.imgbb.com/](https://api.imgbb.com/)
4. 點擊 **「Get API key」**
5. 複製 API Key

> **💡 費用說明：** imgbb 免費帳號提供無限上傳，圖片永久保留（本程式設定 7 天後自動刪除節省空間）。

---

### 第 5 步：設定 GitHub Secrets

1. 前往你 Fork 的 GitHub Repository
2. 點擊上方 **「Settings」** 標籤
3. 左側選單選擇 **「Secrets and variables」→「Actions」**
4. 點擊 **「New repository secret」**，依序新增以下 4 個 Secrets：

| Secret 名稱 | 值 | 說明 |
|-------------|-----|------|
| `GEMINI_API_KEY` | `AIzaSy...` | Google Gemini API Key |
| `LINE_CHANNEL_ACCESS_TOKEN` | `xxx...` | LINE Bot Token |
| `LINE_USER_ID` | `Uxxxxxx...` | 接收者 LINE User ID |
| `IMGBB_API_KEY` | `xxxxx` | imgbb API Key |

**新增方式：**
- **Name**：填入上表的 Secret 名稱（注意大小寫完全相同）
- **Value**：貼上對應的值
- 點擊 **「Add secret」**

---

## 🧪 立即測試

設定完成後，建議先手動觸發一次測試：

1. 前往你的 Repository → **「Actions」** 標籤
2. 左側選擇 **「每日早安圖自動發送」**
3. 點擊右側 **「Run workflow」** → **「Run workflow」**
4. 等待約 1-2 分鐘，查看執行結果
5. 打開 LINE 確認是否收到訊息 🎉

---

## ⏰ 發送時間

系統預設每天 **台灣時間早上 7:00** 自動發送。

若想修改時間，編輯 `.github/workflows/daily_morning.yml`：

```yaml
schedule:
  - cron: "0 23 * * *"   # UTC 時間，台灣 = UTC+8
```

**常用時間對照表：**

| 台灣時間 | UTC Cron 格式 |
|---------|--------------|
| 早上 6:00 | `0 22 * * *` |
| 早上 7:00 | `0 23 * * *` ← 預設 |
| 早上 8:00 | `0 0 * * *` |

---

## 🔧 自訂設定

### 修改語錄

編輯 `quotes.py`，在 `QUOTES` 列表中新增或修改語錄：

```python
{
    "id": 51,                          # 唯一編號
    "quote": "你的自訂語錄",            # 語錄內容
    "author": "作者姓名",               # 作者
    "source": "《出處書名》",            # 出處（可留空 ""）
    "category": "wisdom",              # 分類
    "bg_prompt": "morning sunrise"     # 英文圖片生成提示詞
},
```

**分類選項：** `courage`、`dream`、`perseverance`、`wisdom`、`love`、`growth`、`happiness`

### 發送給多人

修改 `line_sender.py`，新增多個 User ID：

```python
# 在 main.py 中多次呼叫
for user_id in ["Uxxxxxx", "Uyyyyy", "Uzzzzz"]:
    send_morning_image_to_line(image_url, token, user_id, quote)
```

> ⚠️ LINE 免費方案每月限制 200 則訊息（含文字和圖片各算一則）

### 發送至 LINE 群組

將 `LINE_USER_ID` 改為群組 ID（格式：`Cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`，C 開頭）。

取得群組 ID 方式：
1. 將 Bot 加入群組
2. 在群組中傳訊息
3. Webhook 中的 `source.groupId` 即為群組 ID

---

## 🛠️ 本機開發

```bash
# 1. Clone 專案
git clone https://github.com/你的帳號/morning-image-bot.git
cd morning-image-bot

# 2. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 安裝套件
pip install -r requirements.txt

# 4. 設定環境變數
export GEMINI_API_KEY="你的 Key"
export LINE_CHANNEL_ACCESS_TOKEN="你的 Token"
export LINE_USER_ID="你的 User ID"
export IMGBB_API_KEY="你的 Key"

# 5. 執行（發送真實訊息）
python main.py

# 6. 只測試圖片生成（不發送）
python image_generator.py   # 生成 test_output.jpg
```

---

## ❓ 常見問題

**Q: GitHub Actions 每月有免費額度限制嗎？**  
A: GitHub 免費帳號每月有 **2,000 分鐘** 執行額度，本程式每次約用 1-2 分鐘，一年 365 天共約 730 分鐘，完全夠用。

**Q: Gemini 圖片生成失敗怎麼辦？**  
A: 程式已內建備用機制，若 Gemini 失敗會自動改用漸層色背景，確保訊息正常發出。

**Q: LINE 免費方案訊息數量夠用嗎？**  
A: LINE Messaging API 免費方案每月 **200 則**（2025年起調整）。本程式每天發 2 則（文字+圖片），一個月共 60 則，完全免費。發送給多人需計算總則數。

**Q: 圖片中的中文顯示為方塊？**  
A: GitHub Actions 已自動安裝 Noto CJK 字體，本機開發需確認有安裝中文字體。macOS 無需額外安裝。

**Q: 如何停止自動發送？**  
A: 進入 Repository → Actions → 左側選擇 Workflow → 點擊 **「Disable workflow」**

---

## 📄 授權

MIT License — 自由使用、修改、分享

---

## 🙏 致謝

- **Google Gemini** — AI 圖片生成
- **LINE Messaging API** — 訊息推播
- **imgbb** — 免費圖床服務
- **GitHub Actions** — 免費排程服務
