"""
line_sender.py — LINE 訊息推播模組
負責將圖片上傳至 imgbb，並透過 LINE Messaging API 發送
"""

import os
import base64
import requests
import json
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    ImageMessage,
    TextMessage,
    FlexMessage,
    FlexContainer,
)


# ─── imgbb 圖床上傳 ──────────────────────────────────────────────────────────

def upload_to_imgbb(image_bytes: bytes, imgbb_api_key: str) -> str:
    """
    將圖片上傳至 imgbb 並回傳公開 URL
    
    :param image_bytes: 圖片的 bytes 資料
    :param imgbb_api_key: imgbb API Key
    :return: 圖片的公開 URL
    """
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                data={
                    "key": imgbb_api_key,
                    "image": b64_image,
                    "name": f"morning_image_{_today_str()}",
                    "expiration": 604800,  # 7 天後過期（秒）
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                url = data["data"]["url"]
                print(f"✅ 圖片上傳成功: {url}")
                return url
            else:
                raise ValueError(f"imgbb 回應異常: {data}")
        except Exception as e:
            print(f"⚠️  imgbb 上傳第 {attempt + 1} 次失敗: {e}")
            if attempt == 2:
                raise RuntimeError(f"imgbb 上傳失敗，已重試 3 次: {e}")

    return ""


def _today_str() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d")


# ─── LINE 推播 ───────────────────────────────────────────────────────────────

def send_morning_image_to_line(
    image_url: str,
    channel_access_token: str,
    user_id: str,
    quote: dict
) -> bool:
    """
    透過 LINE Messaging API 傳送早安圖片
    
    :param image_url: 圖片的公開 HTTPS URL
    :param channel_access_token: LINE Channel Access Token
    :param user_id: 接收者 LINE User ID（或 Group ID）
    :param quote: 語錄資料（用於附加文字訊息）
    :return: 是否成功
    """
    configuration = Configuration(access_token=channel_access_token)

    with ApiClient(configuration) as api_client:
        line_api = MessagingApi(api_client)

        # 訊息 1：早安問候文字
        from datetime import datetime
        today = datetime.now()
        weekday_map = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
        weekday = weekday_map[today.weekday()]
        date_str = f"{today.month} 月 {today.day} 日，星期{weekday}"

        greeting_text = (
            f"🌅 早安！今天是 {date_str}\n\n"
            f"「{quote['quote']}」\n\n"
            f"— {quote['author']}"
        )
        if quote.get("source"):
            greeting_text += f"，{quote['source']}"
        greeting_text += "\n\n願你今天充滿能量，美好的一天從現在開始！✨"

        # 訊息 2：圖片
        messages = [
            TextMessage(text=greeting_text),
            ImageMessage(
                original_content_url=image_url,
                preview_image_url=image_url,
            ),
        ]

        request = PushMessageRequest(
            to=user_id,
            messages=messages,
        )

        response = line_api.push_message(push_message_request=request)
        print(f"✅ LINE 訊息發送成功，request_id: {response.request_id if hasattr(response, 'request_id') else 'OK'}")
        return True


# ─── 主函式（對外介面）──────────────────────────────────────────────────────

def upload_and_send(
    image_bytes: bytes,
    quote: dict,
    imgbb_api_key: str,
    line_channel_access_token: str,
    line_user_id: str,
) -> bool:
    """
    整合上傳 + 發送的完整流程
    
    :return: 是否成功
    """
    print("📤 上傳圖片至 imgbb...")
    image_url = upload_to_imgbb(image_bytes, imgbb_api_key)

    print("📱 透過 LINE 發送訊息...")
    success = send_morning_image_to_line(
        image_url=image_url,
        channel_access_token=line_channel_access_token,
        user_id=line_user_id,
        quote=quote,
    )
    return success


if __name__ == "__main__":
    # 本機測試（需設定環境變數）
    print("請透過 main.py 執行完整流程")
