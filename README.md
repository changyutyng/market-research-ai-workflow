# 用 AI 做市場研究報告

一套七階段的 AI 協作流程，用來做出**可查證、可被推翻**的市場研究與競品研究。免費版 ChatGPT 就能執行。

**網頁版說明：** https://changyutyng.github.io/market-research-ai-workflow/
（七個階段的 prompt 都有複製按鈕，第一次使用建議從網頁開始）

---

## 為什麼不是一個 prompt

把「幫我研究某個市場」交給 AI，會拿到一份讀起來很完整的報告，但通常缺三樣東西：

1. 它不知道你要用這份研究做什麼決定，所以重要和不重要的內容寫得一樣長
2. 它給的數字和網址有相當比例是捏造的，而且看起來很像真的
3. 它不會區分哪些是查到的、哪些是推論出來的

這套流程把研究拆成七個階段，其中四個階段必須由人停下來檢查。

| 階段 | 做什麼 | 是否停下檢查 |
|---|---|---|
| 1 假設化 | 把「我們相信但沒驗證過的事」列成可檢驗的假設 | **必須停下** |
| 2 對象與判準 | 決定要研究哪些對象、用什麼判準分類 | 快速確認 |
| 3 欄位設計 | 決定每個對象要查證哪些項目 | **必須停下** |
| 4 查證 | 依來源規則上網查資料 | **必須停下** |
| 5 進表 | 把查證結果整理成資料表 | 快速確認 |
| 6 寫文件 | 依據資料表撰寫報告 | 快速確認 |
| 7 審查 | 逐段閱讀，看不懂就提問 | **必須停下** |

---

## 怎麼使用

### 用免費版 ChatGPT

打開[網頁版說明](https://changyutyng.github.io/market-research-ai-workflow/)，照「開始之前」那一節操作即可。重點是**一個階段開一次新對話**，每次先貼「全程規則」，再貼該階段的 prompt。

想看文字檔版本，可以參考 `chatgpt/00_免費版從這裡開始.md` 與 `chatgpt/prompts.md`。

### 用付費版 ChatGPT 建立 Custom GPT

照 `chatgpt/custom-gpt.md` 的步驟操作，約十分鐘。Knowledge 要上傳 `chatgpt/` 資料夾裡的 `source-rules.md`、`field-design.md`、`templates.md`、`failure-modes.md`。

### 用 Claude Code

把 `claude-skill/` 資料夾複製到 `~/.claude/skills/market-research/`，之後輸入 `/market-research` 就能啟用。這個版本附有 `scripts/verify_urls.py`，可以批次檢查查證筆記裡的網址是否有效。

---

## 檔案結構

```
index.html          網頁版說明（GitHub Pages）
chatgpt/            給 ChatGPT 使用者
  00_免費版從這裡開始.md
  prompts.md        全程規則＋七段 prompt
  custom-gpt.md     建立 Custom GPT 的步驟（付費版）
  other-ai.md       用 Projects 或其他 AI 工具的完整說明
  source-rules.md   來源規則與判定三級的定義
  field-design.md   欄位設計規則
  templates.md      資料表與報告的格式
  failure-modes.md  實際發生過的錯誤案例
claude-skill/       Claude Code 的 skill
```

---

## 來源

整理自 2026 年 10 月的一次實際專案：為一個首屆舉辦的小型藝術博覽會做同類市場研究。產出包括 48 頁結論文件、14 個對象 × 30 欄位的對照表、98 筆逐條來源。

作者：changsss
