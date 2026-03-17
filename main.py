"""
main.py — 每日早安圖自動發送系統主程式
執行方式: python main.py
"""

import os
import sys
import traceback
from datetime import datetime

from quotes import get_random_quote
from image_generator import generate_morning_image
from line_sender import upload_and_send


def load_env() -> dict:
    """
    從環境變數讀取設定（GitHub Actions Secrets 會自動注入）
    """
    required_keys = [
        "GEMINI_API_KEY",
        "LINE_CHANNEL_ACCESS_TOKEN",
        "LINE_USER_ID",
        "IMGBB_API_KEY",
    ]
    config = {}
    missing = []

    for key in required_keys:
        value = os.environ.get(key, "").strip()
        if not value:
            missing.append(key)
        config[key] = value

    if missing:
        print(f"❌ 缺少必要的環境變數: {', '.join(missing)}")
        print("請確認 GitHub Secrets 已正確設定（詳見 README.md）")
        sys.exit(1)

    return config


def main():
    print("=" * 60)
    print(f"🌅 每日早安圖系統啟動  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. 讀取設定
    config = load_env()
    print("✅ 環境變數載入成功")

    # 2. 隨機挑選語錄
    quote = get_random_quote()
    print(f"\n📖 今日語錄:")
    print(f"   「{quote['quote']}」")
    print(f"   —— {quote['author']}  {quote.get('source', '')}")
    print(f"   分類: {quote['category']}")

    # 3. 生成早安圖
    print("\n🎨 開始生成早安圖片...")
    try:
        image_bytes = generate_morning_image(
            quote=quote,
            gemini_api_key=config["GEMINI_API_KEY"],
        )
        print(f"✅ 圖片生成完成 ({len(image_bytes) / 1024:.1f} KB)")
    except Exception as e:
        print(f"❌ 圖片生成失敗: {e}")
        traceback.print_exc()
        sys.exit(1)

    # 4. 上傳並發送
    print("\n📱 準備發送至 LINE...")
    try:
        success = upload_and_send(
            image_bytes=image_bytes,
            quote=quote,
            imgbb_api_key=config["IMGBB_API_KEY"],
            line_channel_access_token=config["LINE_CHANNEL_ACCESS_TOKEN"],
            line_user_id=config["LINE_USER_ID"],
        )
        if success:
            print("\n🎉 早安圖發送完成！")
        else:
            print("\n⚠️  發送可能有問題，請檢查 LINE 帳號")
    except Exception as e:
        print(f"❌ 發送失敗: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("=" * 60)
    print("✅ 任務完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
