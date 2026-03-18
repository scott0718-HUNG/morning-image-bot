#!/usr/bin/env python3
"""
每日早安勵志圖自動發送系統
Daily Morning Motivational Image Auto-Sender
"""

import os
import sys
import json
import base64
import time
import io
import requests
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ============================================================
# 名言庫（60 則精選繁體中文勵志名言）
# ============================================================
QUOTES = [
    {"text": "天將降大任於斯人也，必先苦其心志，勞其筋骨，餓其體膚，空乏其身。", "source": "《孟子·告子下》", "author": "孟子"},
    {"text": "路漫漫其修遠兮，吾將上下而求索。", "source": "《離騷》", "author": "屈原"},
    {"text": "千里之行，始於足下。", "source": "《道德經》", "author": "老子"},
    {"text": "學而不思則罔，思而不學則殆。", "source": "《論語·為政》", "author": "孔子"},
    {"text": "人生自古誰無死，留取丹心照汗青。", "source": "《過零丁洋》", "author": "文天祥"},
    {"text": "知之者不如好之者，好之者不如樂之者。", "source": "《論語·雍也》", "author": "孔子"},
    {"text": "不積跬步，無以至千里；不積小流，無以成江海。", "source": "《勸學》", "author": "荀子"},
    {"text": "合抱之木，生於毫末；九層之臺，起於壘土。", "source": "《道德經》", "author": "老子"},
    {"text": "業精於勤，荒於嬉；行成於思，毀於隨。", "source": "《進學解》", "author": "韓愈"},
    {"text": "窮則獨善其身，達則兼善天下。", "source": "《孟子·盡心上》", "author": "孟子"},
    {"text": "生當作人傑，死亦為鬼雄。", "source": "《夏日絕句》", "author": "李清照"},
    {"text": "讀書破萬卷，下筆如有神。", "source": "《奉贈韋左丞丈二十二韻》", "author": "杜甫"},
    {"text": "寶劍鋒從磨礪出，梅花香自苦寒來。", "source": "古訓聯語", "author": "古人"},
    {"text": "君子坦蕩蕩，小人長戚戚。", "source": "《論語·述而》", "author": "孔子"},
    {"text": "捐軀赴國難，視死忽如歸。", "source": "《白馬篇》", "author": "曹植"},
    {"text": "三人行，必有我師焉；擇其善者而從之，其不善者而改之。", "source": "《論語·述而》", "author": "孔子"},
    {"text": "志士仁人，無求生以害仁，有殺身以成仁。", "source": "《論語·衛靈公》", "author": "孔子"},
    {"text": "天下興亡，匹夫有責。", "source": "《日知錄》", "author": "顧炎武"},
    {"text": "聖人不貴尺之璧，而重寸之陰，時難得而易失也。", "source": "《淮南子》", "author": "劉安"},
    {"text": "非淡泊無以明志，非寧靜無以致遠。", "source": "《誡子書》", "author": "諸葛亮"},
    {"text": "落紅不是無情物，化作春泥更護花。", "source": "《己亥雜詩》", "author": "龔自珍"},
    {"text": "海納百川，有容乃大；壁立千仞，無欲則剛。", "source": "林則徐書室聯", "author": "林則徐"},
    {"text": "長風破浪會有時，直掛雲帆濟滄海。", "source": "《行路難》", "author": "李白"},
    {"text": "會當凌絕頂，一覽眾山小。", "source": "《望嶽》", "author": "杜甫"},
    {"text": "沉舟側畔千帆過，病樹前頭萬木春。", "source": "《酬樂天揚州初逢席上見贈》", "author": "劉禹錫"},
    {"text": "山重水複疑無路，柳暗花明又一村。", "source": "《遊山西村》", "author": "陸游"},
    {"text": "老驥伏櫪，志在千里；烈士暮年，壯心不已。", "source": "《龜雖壽》", "author": "曹操"},
    {"text": "古之立大事者，不惟有超世之才，亦必有堅忍不拔之志。", "source": "《晁錯論》", "author": "蘇軾"},
    {"text": "人有悲歡離合，月有陰晴圓缺，此事古難全。", "source": "《水調歌頭》", "author": "蘇軾"},
    {"text": "莫等閒，白了少年頭，空悲切！", "source": "《滿江紅》", "author": "岳飛"},
    {"text": "橫眉冷對千夫指，俯首甘為孺子牛。", "source": "《自嘲》", "author": "魯迅"},
    {"text": "時間是最好的老師，它教會我們寬容，也教會我們珍惜。", "source": "散文集", "author": "三毛"},
    {"text": "我來到這個世界，不是為了生活，而是為了生命。", "source": "《孤獨六講》", "author": "蔣勛"},
    {"text": "人生的意義，在於你給這個世界帶來了什麼，而非你從中取走了什麼。", "source": "演講集", "author": "余光中"},
    {"text": "即使慢，馳而不息，縱令落後，縱令失敗，但必須能夠到達他所向往的目標。", "source": "《且介亭雜文》", "author": "魯迅"},
    {"text": "你若盛開，清風自來。", "source": "現代語錄", "author": "席慕蓉"},
    {"text": "智慧不在於知道答案，而在於知道如何提出問題。", "source": "哲學語錄", "author": "蘇格拉底"},
    {"text": "在你的人生中，你終將成為你所思所想的那種人。", "source": "《論靈魂》", "author": "亞里斯多德"},
    {"text": "想像力比知識更重要，知識是有限的，而想像力可以環抱整個世界。", "source": "訪談錄", "author": "愛因斯坦"},
    {"text": "每一個不曾起舞的日子，都是對生命的辜負。", "source": "《查拉圖斯特拉如是說》", "author": "尼采"},
    {"text": "不是因為有希望才堅持，而是因為堅持才有希望。", "source": "人生格言", "author": "奧勒留"},
    {"text": "你的態度決定你的高度，你的行動決定你的未來。", "source": "現代語錄", "author": "林肯"},
    {"text": "成功不是終點，失敗也不是終結，唯有勇氣才是永恆。", "source": "演說集", "author": "邱吉爾"},
    {"text": "你無法回到過去重新開始，但你可以從今天出發，創造全新的結局。", "source": "人生哲理", "author": "卡內基"},
    {"text": "生命中最重要的不是你處於什麼位置，而是你朝什麼方向前進。", "source": "成功哲學", "author": "霍姆斯"},
    {"text": "每天清晨醒來，你都有兩個選擇：繼續睡覺追逐你的夢，或者起床去實現你的夢。", "source": "勵志語錄", "author": "佚名"},
    {"text": "困難是上天給你最好的禮物，因為它讓你比昨天更強大。", "source": "心靈語錄", "author": "佚名"},
    {"text": "你現在的努力，是在為未來的自己種下最美的樹。", "source": "現代勵志語錄", "author": "佚名"},
    {"text": "最黑暗的時刻，往往是黎明前的一刻。", "source": "人生哲語", "author": "托馬斯·富勒"},
    {"text": "不要等待完美的時機，現在就是最好的時機。", "source": "行動哲學", "author": "拿破崙·希爾"},
    {"text": "一個人能走多遠，取決於他心中的夢有多大。", "source": "勵志文集", "author": "佚名"},
    {"text": "與其感嘆道路坎坷，不如調整步伐繼續前行。", "source": "生活哲語", "author": "佚名"},
    {"text": "改變從此刻開始，一切皆有可能。", "source": "現代語錄", "author": "佚名"},
    {"text": "你比你想像中的更勇敢，你比你看起來更強壯，你比你以為的更聰明。", "source": "《小熊維尼》", "author": "A.A.米爾恩"},
    {"text": "每一次跌倒都是人生給你的提示：你正走在成長的路上。", "source": "心靈語錄", "author": "佚名"},
    {"text": "人生沒有白走的路，每一步都算數。", "source": "現代勵志語錄", "author": "佚名"},
    {"text": "讓你的夢想大過你的恐懼，讓你的行動大過你的顧慮。", "source": "成功學語錄", "author": "Robin Sharma"},
    {"text": "播下行動的種子，收穫習慣的果實；播下習慣的種子，收穫品格的果實。", "source": "《人性的弱點》", "author": "卡內基"},
    {"text": "不管昨天發生了什麼，不管昨天的自己有多糟糕，今天請重新出發。", "source": "心靈雞湯", "author": "佚名"},
    {"text": "相信自己，你比你以為的更有力量。", "source": "勵志語錄", "author": "佚名"},
    {"text": "晨起時，感謝這一天的到來；每天都是新的機會，每天都是新的開始。", "source": "冥想語錄", "author": "佚名"},
]

# ============================================================
# AI 圖片 Prompt 關鍵字對應
# ============================================================
PROMPT_THEMES = {
    "奮鬥": "person climbing mountain at sunrise, determination, golden light",
    "學習": "student reading book in peaceful garden, morning light, cherry blossoms",
    "堅持": "lone tree standing in storm, resilient, dramatic sky",
    "夢想": "person standing on hilltop gazing at stars, dreamy night sky, milky way",
    "自然": "misty mountain forest path, morning fog, peaceful, ethereal",
    "希望": "sunrise over ocean horizon, golden hour, warm light, hopeful",
    "愛國": "mountain landscape with clouds, majestic, patriotic",
    "時間": "hourglass with flower petals, soft morning light, contemplative",
    "成功": "person on mountain peak, sunrise, achievement, vast landscape",
    "人生": "winding road through autumn forest, journey, warm colors",
    "default": "beautiful misty mountain landscape at sunrise, golden hour, realistic, cinematic"
}

def get_prompt_for_quote(quote_text):
    """根據名言內容生成適合的圖片 prompt"""
    for keyword, prompt in PROMPT_THEMES.items():
        if keyword in quote_text:
            return prompt
    return PROMPT_THEMES["default"]


# ============================================================
# 輔助工具函式
# ============================================================
def get_taiwan_time():
    """取得台灣時間（UTC+8）"""
    tz_taiwan = timezone(timedelta(hours=8))
    return datetime.now(tz_taiwan)


def get_today_quote():
    """依今日日期選取名言"""
    now = get_taiwan_time()
    index = (now.year + now.month + now.day) % len(QUOTES)
    return QUOTES[index]


def format_date_chinese(dt):
    """格式化為繁體中文日期"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[dt.weekday()]
    return f"{dt.year}年{dt.month}月{dt.day}日　{weekday}"


def retry_request(func, retries=3, delay=5):
    """帶重試機制的請求執行器"""
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"  ⚠ 嘗試 {attempt + 1}/{retries} 失敗：{e}")
            if attempt < retries - 1:
                time.sleep(delay)
    raise Exception(f"所有 {retries} 次嘗試均失敗")


# ============================================================
# 字型下載與載入
# ============================================================
def download_font():
    """下載 Noto Sans TC 中文字型"""
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    os.makedirs(font_dir, exist_ok=True)
    font_path = os.path.join(font_dir, "NotoSansTC-Bold.ttf")

    if os.path.exists(font_path):
        print("✓ 字型已存在")
        return font_path

    print("⬇ 下載中文字型...")
    url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Bold.otf"
    # 備用 URL
    fallback_url = "https://fonts.gstatic.com/ea/notosanstc/v1/NotoSansTC-Bold.otf"

    for font_url in [url, fallback_url]:
        try:
            resp = requests.get(font_url, timeout=60)
            if resp.status_code == 200:
                with open(font_path, 'wb') as f:
                    f.write(resp.content)
                print(f"✓ 字型下載完成（{len(resp.content)//1024}KB）")
                return font_path
        except Exception as e:
            print(f"  字型下載失敗（{font_url}）：{e}")

    print("⚠ 使用系統預設字型")
    return None


def get_fonts(font_path, image_size=1080):
    """載入各尺寸字型"""
    try:
        if font_path and os.path.exists(font_path):
            return {
                'date': ImageFont.truetype(font_path, 42),
                'quote_large': ImageFont.truetype(font_path, 54),
                'quote_medium': ImageFont.truetype(font_path, 44),
                'quote_small': ImageFont.truetype(font_path, 36),
                'source': ImageFont.truetype(font_path, 30),
            }
    except Exception as e:
        print(f"⚠ 字型載入失敗：{e}，使用預設字型")

    # 系統備用字型（Ubuntu）
    system_fonts = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for sf in system_fonts:
        if os.path.exists(sf):
            try:
                return {
                    'date': ImageFont.truetype(sf, 42),
                    'quote_large': ImageFont.truetype(sf, 54),
                    'quote_medium': ImageFont.truetype(sf, 44),
                    'quote_small': ImageFont.truetype(sf, 36),
                    'source': ImageFont.truetype(sf, 30),
                }
            except Exception:
                continue

    # 最後備用：PIL 內建字型
    default = ImageFont.load_default()
    return {k: default for k in ['date', 'quote_large', 'quote_medium', 'quote_small', 'source']}


# ============================================================
# AI 圖片生成（Pollinations.ai - 完全免費）
# ============================================================
def generate_background_image(prompt, seed=42):
    """使用 Pollinations.ai 生成背景圖片"""
    print(f"🎨 生成 AI 背景圖片...")
    print(f"   Prompt: {prompt}")

    full_prompt = (
        f"{prompt}, ultra realistic photography, cinematic lighting, "
        f"beautiful composition, 8k resolution, masterpiece, "
        f"warm golden hour lighting, professional photography"
    )
    encoded_prompt = requests.utils.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&seed={seed}&nologo=true"

    def fetch():
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200 and len(resp.content) > 1000:
            return Image.open(io.BytesIO(resp.content)).convert("RGB")
        raise Exception(f"HTTP {resp.status_code}")

    try:
        img = retry_request(fetch, retries=2, delay=5)
        print(f"✓ AI 圖片生成成功（{img.size}）")
        return img
    except Exception as e:
        print(f"⚠ AI 生圖失敗：{e}，使用漸層備案")
        return create_gradient_background()


def create_gradient_background():
    """建立美麗漸層背景作為備案"""
    img = Image.new('RGB', (1080, 1080))
    draw = ImageDraw.Draw(img)

    # 藍紫金漸層
    colors = [
        (15, 32, 80),   # 深藍
        (44, 62, 120),  # 藍
        (85, 40, 100),  # 紫
        (140, 80, 60),  # 橙紫
        (200, 120, 40), # 金橙
    ]

    for y in range(1080):
        ratio = y / 1080
        idx = min(int(ratio * (len(colors) - 1)), len(colors) - 2)
        local = ratio * (len(colors) - 1) - idx
        c1, c2 = colors[idx], colors[idx + 1]
        r = int(c1[0] + (c2[0] - c1[0]) * local)
        g = int(c1[1] + (c2[1] - c1[1]) * local)
        b = int(c1[2] + (c2[2] - c1[2]) * local)
        draw.line([(0, y), (1080, y)], fill=(r, g, b))

    return img


# ============================================================
# 圖片合成
# ============================================================
def wrap_text(text, font, max_width, draw):
    """自動斷行，支援中文"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] > max_width and current:
            lines.append(current)
            current = char
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def draw_text_with_outline(draw, pos, text, font, fill, outline_color, outline_width=3, shadow=True):
    """繪製帶輪廓線和陰影的文字"""
    x, y = pos
    # 陰影
    if shadow:
        draw.text((x + 4, y + 4), text, font=font, fill=(0, 0, 0, 160))
    # 輪廓
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # 主體文字
    draw.text(pos, text, font=font, fill=fill)


def compose_image(bg_image, quote, date_str, font_path):
    """合成最終早安圖"""
    img = bg_image.copy().resize((1080, 1080), Image.LANCZOS)

    # 微調背景對比度
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = ImageEnhance.Brightness(img).enhance(0.85)

    # 建立半透明漸層遮罩（讓文字更清晰）
    overlay = Image.new('RGBA', (1080, 1080), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # 上方漸層（日期區）
    for y in range(180):
        alpha = int(160 * (1 - y / 180))
        draw_ov.line([(0, y), (1080, y)], fill=(0, 0, 0, alpha))

    # 下方漸層（出處區）
    for y in range(880, 1080):
        alpha = int(160 * ((y - 880) / 200))
        draw_ov.line([(0, y), (1080, y)], fill=(0, 0, 0, alpha))

    # 中央輕度遮罩（名言背景）
    draw_ov.rectangle([(60, 280), (1020, 760)], fill=(0, 0, 0, 90))

    # 合併圖層
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)
    img = img.convert('RGB')

    draw = ImageDraw.Draw(img, 'RGBA')
    fonts = get_fonts(font_path)

    # ---- 左上角日期 ----
    date_x, date_y = 50, 40
    draw_text_with_outline(
        draw, (date_x, date_y), date_str,
        fonts['date'], (255, 255, 255), (0, 0, 0), outline_width=2
    )

    # ---- 大裝飾引號 ----
    try:
         deco_font = ImageFont.truetype(font_path, 180) if font_path else fonts['quote_large']
    #    draw.text((50, 250), "「", font=deco_font, fill=(255, 255, 255, 40))
    #    draw.text((900, 550), "」", font=deco_font, fill=(255, 255, 255, 40))
    except Exception:
        pass

    # ---- 名言文字（自動選擇字型大小）----
    text = quote['text']
    max_width = 880

    # 選擇最合適的字型大小
    selected_font = fonts['quote_large']
    for fname in ['quote_large', 'quote_medium', 'quote_small']:
        test_font = fonts[fname]
        lines = wrap_text(text, test_font, max_width, draw)
        if len(lines) <= 5:
            selected_font = test_font
            break

    lines = wrap_text(text, selected_font, max_width, draw)

    # 計算名言區域垂直置中
    line_height = draw.textbbox((0, 0), "測", font=selected_font)[3] + 18
    total_height = len(lines) * line_height
    y_start = (1080 - total_height) // 2 - 30

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=selected_font)
        line_width = bbox[2] - bbox[0]
        x = (1080 - line_width) // 2
        y = y_start + i * line_height
        draw_text_with_outline(
            draw, (x, y), line, selected_font,
            (255, 255, 255), (0, 0, 0), outline_width=3
        )

    # ---- 底部出處 ----
    source_text = f"—— {quote['source']}　{quote['author']}"
    bbox = draw.textbbox((0, 0), source_text, font=fonts['source'])
    src_x = (1080 - (bbox[2] - bbox[0])) // 2
    src_y = 930
    draw_text_with_outline(
        draw, (src_x, src_y), source_text,
        fonts['source'], (255, 240, 200), (0, 0, 0), outline_width=2
    )

    # ---- 右下角小標記 ----
    mark_text = "錦男的祝福"
    try:
        mark_font = ImageFont.truetype(font_path, 22) if font_path else fonts['source']
        draw.text((900, 1040), mark_text, font=mark_font, fill=(255, 255, 255, 160))
    except Exception:
        pass

    print("✓ 圖片合成完成")
    return img


# ============================================================
# ImgBB 圖片上傳
# ============================================================
def upload_to_imgbb(image, api_key):
    """上傳圖片至 ImgBB，回傳圖片 URL"""
    print("⬆ 上傳圖片至 ImgBB...")

    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=95)
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode('utf-8')

    def upload():
        resp = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": api_key, "image": img_data},
            timeout=30
        )
        result = resp.json()
        if result.get("success"):
            url = result["data"]["url"]
            print(f"✓ 上傳成功：{url}")
            return url
        raise Exception(f"上傳失敗：{result}")

    return retry_request(upload)


# ============================================================
# LINE Messaging API 推播
# ============================================================
def send_line_image(image_url, channel_token, user_id, quote):
    """透過 LINE Messaging API 傳送圖片訊息"""
    print(f"📲 傳送 LINE 訊息至 {user_id[:8]}...")

    # 同時傳送圖片 + 名言文字訊息
    now = get_taiwan_time()
    date_str = format_date_chinese(now)
    caption = f"🌅 {date_str}\n\n「{quote['text']}」\n\n—— {quote['source']}　{quote['author']}"

    messages = [
        {
            "type": "image",
            "originalContentUrl": image_url,
            "previewImageUrl": image_url
        },
        {
            "type": "text",
            "text": caption
        }
    ]

    def send():
        resp = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={
                "Authorization": f"Bearer {channel_token}",
                "Content-Type": "application/json"
            },
            json={"to": user_id, "messages": messages},
            timeout=30
        )
        if resp.status_code == 200:
            print("✓ LINE 訊息傳送成功！")
            return True
        raise Exception(f"HTTP {resp.status_code}：{resp.text}")

    return retry_request(send)


# ============================================================
# 主程式
# ============================================================
def main():
    print("=" * 60)
    print("🌅 每日早安勵志圖自動發送系統")
    print("=" * 60)

    # 1. 讀取環境變數
    imgbb_key = os.environ.get("IMGBB_API_KEY")
    line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    line_user_ids = os.environ.get("LINE_USER_ID", "")

    if not all([imgbb_key, line_token, line_user_ids]):
        print("❌ 錯誤：缺少必要環境變數")
        print("   需要：IMGBB_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID")
        sys.exit(1)

    user_ids = [uid.strip() for uid in line_user_ids.split(",") if uid.strip()]

    # 2. 取得今日資訊
    now = get_taiwan_time()
    date_str = format_date_chinese(now)
    quote = get_today_quote()
    seed = now.year * 10000 + now.month * 100 + now.day

    print(f"\n📅 日期：{date_str}")
    print(f"💬 名言：{quote['text']}")
    print(f"   出處：{quote['source']} / {quote['author']}")
    print(f"👥 推播人數：{len(user_ids)} 人")
    print()

    # 3. 下載字型
    font_path = download_font()
    print()

    # 4. 生成 AI 背景圖
    prompt = get_prompt_for_quote(quote['text'])
    bg_image = generate_background_image(prompt, seed=seed)
    print()

    # 5. 合成圖片
    print("🖼 合成早安圖...")
    final_image = compose_image(bg_image, quote, date_str, font_path)
    print()

    # 6. 上傳至 ImgBB
    image_url = upload_to_imgbb(final_image, imgbb_key)
    print()

    # 7. 發送 LINE 訊息
    for uid in user_ids:
        send_line_image(image_url, line_token, uid, quote)
    print()

    print("=" * 60)
    print("✅ 執行完成！")
    print(f"   名言：{quote['text'][:20]}...")
    print(f"   圖片：{image_url}")
    print("=" * 60)


if __name__ == "__main__":
    main()
