import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

PROMPT = """You are a food identification and nutrition expert.

Look at this image carefully.

Step 1: Determine if this image contains food or a beverage intended for human consumption.

Step 2: If it does NOT contain food, respond with EXACTLY this text and nothing else:
NOT_FOOD

Step 3: If it DOES contain food, respond in this exact format (start with FOOD_DETECTED on the first line):
FOOD_DETECTED
食物名稱: [食物或料理的名稱]
估計熱量: [數字] 大卡
份量假設: [簡短描述假設的份量]
信心程度: [低/中/高]
備註: [任何重要說明，例如「視烹調方式而定差異較大」]"""


def analyze_food(api_key: str, image) -> str:
    if not api_key or not api_key.strip():
        return "請輸入 Google Gemini API Key"
    if image is None:
        return "請上傳一張圖片"

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([PROMPT, image])
        result_text = response.text.strip()

        if result_text.startswith("NOT_FOOD"):
            return "這個不是食物"
        elif result_text.startswith("FOOD_DETECTED"):
            lines = result_text.split("\n")[1:]
            return "\n".join(lines).strip()
        else:
            return result_text

    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
            return "API Key 無效，請確認後重試"
        elif "quota" in error_msg.lower():
            return "API 配額已用盡，請稍後再試"
        else:
            return f"發生錯誤: {error_msg}"


def build_ui():
    with gr.Blocks(title="食物卡路里估算器") as demo:
        gr.Markdown("# 🍱 食物卡路里估算器")
        gr.Markdown("上傳食物照片，AI 將識別食物並估算卡路里。")

        with gr.Row():
            with gr.Column():
                api_key_input = gr.Textbox(
                    label="Google Gemini API Key",
                    placeholder="AIza...",
                    type="password",
                    value=os.environ.get("GOOGLE_API_KEY", ""),
                )
                image_input = gr.Image(
                    label="上傳食物圖片",
                    type="pil",
                )
                submit_btn = gr.Button("分析", variant="primary")

            with gr.Column():
                output = gr.Textbox(
                    label="分析結果",
                    lines=8,
                    interactive=False,
                )

        submit_btn.click(
            fn=analyze_food,
            inputs=[api_key_input, image_input],
            outputs=output,
        )

    return demo


demo = build_ui()

if __name__ == "__main__":
    demo.launch()
