"""
image_generator.py — 早安圖片生成模組
使用 Gemini Imagen API 生成背景圖，再用 Pillow 合成文字
"""

import os
import io
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import google.generativeai as genai
import requests


# ─── 常數設定 ────────────────────────────────────────────────────────────────

IMAGE_SIZE = (1080, 1080)
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

# 嘗試的字體路徑（依優先順序）
FONT_PATHS = [
    os.path.join(FONT_DIR, "NotoSansTC-Bold.ttf"),
    "/usr/share/fonts/truetype/noto/NotoSansTC-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]

WEEKDAY_MAP = {
    0: "一", 1: "二", 2: "三", 3: "四",
    4: "五", 5: "六", 6: "日"
}


# ─── 字體載入 ────────────────────────────────────────────────────────────────

def _load_font(size: int) -> ImageFont.FreeTypeFont:
    """嘗試載入支援中文的字體"""
    for path in FONT_PATHS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # 找不到字體時回退至預設字體
    return ImageFont.load_default()


# ─── Gemini 圖片生成 ─────────────────────────────────────────────────────────

def generate_background(prompt: str, api_key: str) -> Image.Image:
    """
    使用 Gemini Imagen 3 生成背景圖片
    若失敗，回退至漸層色背景
    """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=(
                f"{prompt}, "
                "beautiful morning atmosphere, golden hour lighting, "
                "inspiring and uplifting mood, high quality, 4K, "
                "no text, no watermarks, photorealistic"
            ),
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="block_only_high",
            ),
        )
        image_bytes = response.generated_images[0].image.image_bytes
        return Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(IMAGE_SIZE)

    except Exception as e:
        print(f"⚠️  Gemini 圖片生成失敗，改用漸層背景: {e}")
        return _create_gradient_background()


def _create_gradient_background() -> Image.Image:
    """建立備用的漸層背景（橙紅晨光風格）"""
    img = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(img)
    colors = [
        (255, 94, 58),   # 橙紅（頂部）
        (255, 165, 0),   # 橘黃（中上）
        (255, 200, 50),  # 金黃（中下）
        (135, 206, 235), # 天藍（底部）
    ]
    height = IMAGE_SIZE[1]
    section = height // (len(colors) - 1)
    for i in range(len(colors) - 1):
        r1, g1, b1 = colors[i]
        r2, g2, b2 = colors[i + 1]
        for y in range(section):
            ratio = y / section
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(0, i * section + y), (IMAGE_SIZE[0], i * section + y)],
                      fill=(r, g, b))
    return img


# ─── 圖片合成 ────────────────────────────────────────────────────────────────

def add_overlay(img: Image.Image) -> Image.Image:
    """疊加半透明暗色漸層遮罩，讓文字更清晰"""
    overlay = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # 中央到邊緣漸層
    for y in range(IMAGE_SIZE[1]):
        ratio = abs(y - IMAGE_SIZE[1] / 2) / (IMAGE_SIZE[1] / 2)
        alpha = int(140 * ratio + 40)
        draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=(0, 0, 0, alpha))
    # 合成
    base = img.convert("RGBA")
    result = Image.alpha_composite(base, overlay)
    return result.convert("RGB")


def _draw_text_with_shadow(draw, pos, text, font, fill, shadow_offset=3, shadow_color=(0, 0, 0, 180)):
    """繪製帶陰影的文字"""
    x, y = pos
    # 陰影（多方向，更柔和）
    for dx, dy in [(-shadow_offset, -shadow_offset), (shadow_offset, shadow_offset),
                   (-shadow_offset, shadow_offset), (shadow_offset, -shadow_offset)]:
        draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)
    # 主要文字
    draw.text((x, y), text, font=font, fill=fill)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """根據圖片寬度自動換行"""
    # 中文每字寬度大致等於字號，用 textwrap 估算
    lines = []
    # 先判斷是否以中文為主
    is_cjk = any('\u4e00' <= c <= '\u9fff' for c in text)

    if is_cjk:
        # 中文：按字元數換行
        char_per_line = max(1, max_width // font.size)
        lines = textwrap.wrap(text, width=char_per_line, break_long_words=True)
    else:
        # 英文：按空格換行
        words = text.split()
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

    return lines if lines else [text]


def compose_image(bg_image: Image.Image, quote: dict, date: datetime) -> Image.Image:
    """
    合成完整早安圖
    
    :param bg_image: 背景圖片
    :param quote: 語錄資料 dict
    :param date: 日期
    :return: 合成後的圖片
    """
    img = add_overlay(bg_image)
    draw = ImageDraw.Draw(img, "RGBA")

    W, H = IMAGE_SIZE

    # ── 字體 ──────────────────────────────────────────────────────────────────
    font_date    = _load_font(30)
    font_greeting = _load_font(52)
    font_quote   = _load_font(42)
    font_author  = _load_font(30)
    font_source  = _load_font(24)

    # ── 左上角日期標籤 ────────────────────────────────────────────────────────
    weekday = WEEKDAY_MAP[date.weekday()]
    date_str = f"  {date.year} 年 {date.month:02d} 月 {date.day:02d} 日  星期{weekday}  "

    date_bbox = draw.textbbox((0, 0), date_str, font=font_date)
    label_w = date_bbox[2] - date_bbox[0] + 20
    label_h = date_bbox[3] - date_bbox[1] + 20

    # 半透明圓角黑底
    label_img = Image.new("RGBA", (label_w + 20, label_h + 20), (0, 0, 0, 0))
    label_draw = ImageDraw.Draw(label_img)
    label_draw.rounded_rectangle(
        [(0, 0), (label_w + 18, label_h + 18)],
        radius=14,
        fill=(0, 0, 0, 160)
    )
    img_rgba = img.convert("RGBA")
    img_rgba.paste(label_img, (30, 30), label_img)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.text((44, 44), date_str, font=font_date, fill=(255, 255, 255, 230))

    # ── 早安標語 ──────────────────────────────────────────────────────────────
    greeting = "🌅  早  安"
    g_bbox = draw.textbbox((0, 0), greeting, font=font_greeting)
    g_w = g_bbox[2] - g_bbox[0]
    _draw_text_with_shadow(
        draw,
        ((W - g_w) // 2, 160),
        greeting,
        font_greeting,
        fill=(255, 245, 200),
        shadow_offset=3
    )

    # ── 分隔線 ────────────────────────────────────────────────────────────────
    line_y = 240
    line_x1, line_x2 = W // 4, 3 * W // 4
    draw.line([(line_x1, line_y), (line_x2, line_y)], fill=(255, 255, 255, 180), width=2)

    # ── 語錄文字（自動換行，垂直置中）────────────────────────────────────────
    quote_text = f"「 {quote['quote']} 」"
    max_text_width = W - 120
    lines = _wrap_text(quote_text, font_quote, max_text_width)
    line_height = font_quote.size + 16
    total_text_h = len(lines) * line_height

    start_y = (H - total_text_h) // 2 - 30
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_quote)
        lw = bbox[2] - bbox[0]
        _draw_text_with_shadow(
            draw,
            ((W - lw) // 2, start_y + i * line_height),
            line,
            font_quote,
            fill=(255, 255, 255),
            shadow_offset=3
        )

    # ── 作者 ──────────────────────────────────────────────────────────────────
    author_y = start_y + total_text_h + 30
    author_text = f"—— {quote['author']}"
    if quote.get("source"):
        author_text += f"  《{quote['source'].strip('《》')}》"

    a_bbox = draw.textbbox((0, 0), author_text, font=font_author)
    aw = a_bbox[2] - a_bbox[0]
    _draw_text_with_shadow(
        draw,
        ((W - aw) // 2, author_y),
        author_text,
        font_author,
        fill=(255, 215, 0),   # 金色
        shadow_offset=2
    )

    # ── 底部品牌標記 ──────────────────────────────────────────────────────────
    brand = "✨ 每日早安 · 願你今天充滿能量 ✨"
    b_bbox = draw.textbbox((0, 0), brand, font=font_source)
    bw = b_bbox[2] - b_bbox[0]
    draw.text(((W - bw) // 2, H - 60), brand, font=font_source,
              fill=(255, 255, 255, 180))

    return img


# ─── 主函式（對外介面）──────────────────────────────────────────────────────

def generate_morning_image(quote: dict, gemini_api_key: str) -> bytes:
    """
    產生完整早安圖，回傳 JPEG bytes
    
    :param quote: 語錄 dict
    :param gemini_api_key: Gemini API Key
    :return: JPEG image bytes
    """
    today = datetime.now()

    print(f"🎨 正在使用 Gemini 生成背景圖片...")
    bg = generate_background(quote.get("bg_prompt", "beautiful morning sunrise landscape"), gemini_api_key)

    print(f"✏️  正在合成文字...")
    final_img = compose_image(bg, quote, today)

    # 輸出為 JPEG bytes
    output = io.BytesIO()
    final_img.save(output, format="JPEG", quality=95)
    output.seek(0)
    return output.getvalue()


if __name__ == "__main__":
    # 本機測試
    from quotes import get_random_quote
    quote = get_random_quote()
    api_key = os.environ.get("GEMINI_API_KEY", "")
    img_bytes = generate_morning_image(quote, api_key)
    with open("test_output.jpg", "wb") as f:
        f.write(img_bytes)
    print("✅ 測試圖片已儲存為 test_output.jpg")
