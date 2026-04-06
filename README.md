---
title: Food Calorie Estimator
emoji: 🍱
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 5.23.3
app_file: app.py
pinned: false
license: mit
---

# 食物卡路里估算器

上傳食物照片，AI 將識別食物並估算卡路里。
使用 Google Gemini 視覺模型驅動。

## 使用方式
1. 在欄位中輸入你的 Google Gemini API Key
2. 上傳一張食物照片
3. 點擊「分析」

## 注意事項
- 若圖片中沒有食物，應用程式將回應「這個不是食物」
- 熱量估算為近似值，僅供參考
- 在 HuggingFace Spaces 部署時，可在 Space Settings → Repository secrets 設定 `GOOGLE_API_KEY`，系統會自動填入欄位
