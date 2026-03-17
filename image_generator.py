"""
image_generator.py — 早安圖片生成模組
使用 Gemini 2.0 Flash Preview（免費）生成背景圖，再用 Pillow 合成文字
"""

import os
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types


IMAGE_SIZE = (1080, 1080)
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

FONT_PATHS = [
    os.path.join(FONT_DIR, "NotoSansTC-Bold.ttf"),
    "/usr/share/fonts/truetype/noto/NotoSansTC-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]

WEEKDAY_MAP = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}


# ─── 字體 ────────────────────────────────────────────────────────────────────

def _load_font(size: int):
    for path in FONT_PATHS:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ─── Gemini 圖片生成 ──────────────────────────────────────────────────────────

def generate_background(prompt: str, api_key: str) -> Image.Image:
    """
    使用 google-genai 新版 SDK
    模型：gemini-2.0-flash-preview-image-generation（免費額度支援）
    """
    try:
        client = genai.Client(api_key=api_key)

        full_prompt = (
            f"{prompt}, "
            "beautiful Chinese morning atmosphere, golden hour sunrise lighting, "
            "inspiring and uplifting mood, high quality photorealistic landscape, "
            "no text, no watermarks, no people"
        )

        print("🎨 送出 Gemini 圖片生成請求...")

        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                img = Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
                img = img.resize(IMAGE_SIZE, Image.LANCZOS)
                print("✅ Gemini 背景圖片生成成功")
                return img

        raise ValueError("回應中未找到圖片資料")

    except Exception as e:
        print(f"⚠️  Gemini 失敗，改用備用漸層背景: {e}")
        return _create_gradient_background()


# ─── 備用漸層背景 ─────────────────────────────────────────────────────────────

def _create_gradient_background() -> Image.Image:
    img  = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(img)
    top, mid, bottom = (25, 15, 60), (210, 70, 20), (255, 175, 50)
    H = IMAGE_SIZE[1]
    for y in range(H):
        if y < H // 2:
            r = y / (H // 2)
            c = tuple(int(top[i] + (mid[i] - top[i]) * r) for i in range(3))
        else:
            r = (y - H // 2) / (H // 2)
            c = tuple(int(mid[i] + (bottom[i] - mid[i]) * r) for i in range(3))
        draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=c)
    ov = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    cx, cy = IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 3
    for radius in range(280, 0, -4):
        alpha = int(55 * (1 - radius / 280))
        od.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)],
                   fill=(255, 220, 100, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


# ─── 合成工具 ─────────────────────────────────────────────────────────────────

def _add_overlay(img: Image.Image) -> Image.Image:
    ov   = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)
    H = IMAGE_SIZE[1]
    for y in range(H):
        ratio = abs(y - H / 2) / (H / 2)
        alpha = int(150 * ratio + 30)
        draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def _shadow_text(draw, pos, text, font, fill=(255, 255, 255), s=3):
    x, y = pos
    for dx in range(-s, s + 1):
        for dy in range(-s, s + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=font, fill=fill)


def _wrap_cjk(text: str, font, max_width: int) -> list:
    lines, current = [], ""
    for char in text:
        test = current + char
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = char
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# ─── 主合成函式 ───────────────────────────────────────────────────────────────

def compose_image(bg: Image.Image, quote: dict, date: datetime) -> Image.Image:
    img  = _add_overlay(bg)
    draw = ImageDraw.Draw(img, "RGBA")
    W, H = IMAGE_SIZE

    font_date     = _load_font(30)
    font_greeting = _load_font(54)
    font_quote    = _load_font(44)
    font_author   = _load_font(30)
    font_brand    = _load_font(24)

    # ── 左上角日期標籤 ────────────────────────────────────────────────────────
    weekday  = WEEKDAY_MAP[date.weekday()]
    date_str = f"  {date.year} 年 {date.month:02d} 月 {date.day:02d} 日  星期{weekday}  "
    bbox     = font_date.getbbox(date_str)
    lw, lh   = bbox[2] - bbox[0] + 24, bbox[3] - bbox[1] + 24
    label    = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ld       = ImageDraw.Draw(label)
    ld.rounded_rectangle([(0, 0), (lw - 1, lh - 1)], radius=12, fill=(0, 0, 0, 155))
    base     = img.convert("RGBA")
    base.paste(label, (30, 30), label)
    img      = base.convert("RGB")
    draw     = ImageDraw.Draw(img)
    draw.text((42, 42), date_str, font=font_date, fill=(255, 255, 255))

    # ── 早安標語 ──────────────────────────────────────────────────────────────
    greeting = "🌅  早  安"
    gw = font_greeting.getbbox(greeting)[2]
    _shadow_text(draw, ((W - gw) // 2, 150), greeting, font_greeting,
                 fill=(255, 245, 180), s=3)

    # ── 分隔線 ────────────────────────────────────────────────────────────────
    draw.line([(W // 4, 235), (3 * W // 4, 235)], fill=(255, 255, 255, 180), width=2)

    # ── 語錄文字 ──────────────────────────────────────────────────────────────
    quote_text = f"「{quote['quote']}」"
    lines      = _wrap_cjk(quote_text, font_quote, W - 120)
    line_h     = font_quote.size + 18
    total_h    = len(lines) * line_h
    start_y    = (H - total_h) // 2 - 20

    for i, line in enumerate(lines):
        lw2 = font_quote.getbbox(line)[2]
        _shadow_text(draw, ((W - lw2) // 2, start_y + i * line_h),
                     line, font_quote, fill=(255, 255, 255), s=3)

    # ── 作者 ──────────────────────────────────────────────────────────────────
    author_text = f"—— {quote['author']}"
    if quote.get("source"):
        author_text += f"  《{quote['source'].strip('《》')}》"
    aw = font_author.getbbox(author_text)[2]
    _shadow_text(draw, ((W - aw) // 2, start_y + total_h + 32),
                 author_text, font_author, fill=(255, 215, 0), s=2)

    # ── 底部品牌 ──────────────────────────────────────────────────────────────
    brand = "✨ 每日早安 · 願你今天充滿能量 ✨"
    bw    = font_brand.getbbox(brand)[2]
    draw.text(((W - bw) // 2, H - 58), brand, font=font_brand,
              fill=(255, 255, 255, 180))

    return img


# ─── 對外主函式 ───────────────────────────────────────────────────────────────

def generate_morning_image(quote: dict, gemini_api_key: str) -> bytes:
    today = datetime.now()
    print("🎨 正在使用 Gemini 2.0 Flash 生成背景圖片...")
    bg    = generate_background(
        quote.get("bg_prompt", "serene Chinese mountain sunrise"), gemini_api_key)
    print("✏️  正在合成文字圖層...")
    final = compose_image(bg, quote, today)
    out   = io.BytesIO()
    final.save(out, format="JPEG", quality=95)
    out.seek(0)
    return out.getvalue()


if __name__ == "__main__":
    from quotes import get_random_quote
    q   = get_random_quote()
    key = os.environ.get("GEMINI_API_KEY", "")
    with open("test_output.jpg", "wb") as f:
        f.write(generate_morning_image(q, key))
    print("✅ 測試圖片已儲存為 test_output.jpg")
