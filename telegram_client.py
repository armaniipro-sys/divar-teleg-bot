
"""Telegram bot setup and message formatting/sending."""
import html

import telegram

import config
from hashtags import generate_hashtags


req_proxy = telegram.request.HTTPXRequest(
    proxy_url=config.PROXY_URL,
    connect_timeout=30,
    read_timeout=30,
    write_timeout=30,
    pool_timeout=30,
)

bot = telegram.Bot(
    token=config.BOT_TOKEN,
    request=req_proxy,
)


def build_message_text(ad) -> str:
    text = f"🗄 <b>{html.escape(ad.title)}</b>\n"

    location_line = ad.posted_in or ad.district
    if location_line:
        text += f"📌 محل آگهی: <i>{html.escape(location_line)}</i>\n"

    price = f"{ad.price:,} تومان" if ad.price else "توافقی"
    text += f"💰 قیمت: {price}\n"

    if ad.features:
        text += "\n📋 <b>مشخصات:</b>\n"
        for label, value in ad.features:
            text += (
                f"🔸 {html.escape(str(label))}: "
                f"{html.escape(str(value))}\n"
            )

    if ad.description:
        text += (
            f"\n📄 <b>توضیحات:</b>\n"
            f"{html.escape(ad.description)}"
        )

    hashtags = generate_hashtags(ad)
    if hashtags:
        text += "\n\n" + " ".join(
            f"#{tag}" for tag in hashtags
        )

    text += config.FOOTER_TEXT

    return text


async def send_telegram_message(ad):
    """Send ad images and text separately."""

    text = build_message_text(ad)

    # Send images first.
    images = ad.images or []

    if len(images) == 1:
        await bot.send_photo(
            chat_id=config.BOT_CHATID,
            photo=images[0],
        )

    elif len(images) > 1:
        media_list = [
            telegram.InputMediaPhoto(img)
            for img in images[:10]
        ]

        await bot.send_media_group(
            chat_id=config.BOT_CHATID,
            media=media_list,
        )

    # Send text separately to avoid photo caption limits.
    # Keep every message below Telegram's 4096-character limit.
    limit = 4000

    while text:
        chunk = text[:limit]

        if len(text) > limit:
            split_at = chunk.rfind("\n")
            if split_at > 0:
                chunk = chunk[:split_at]

        await bot.send_message(
            chat_id=config.BOT_CHATID,
            text=chunk,
            parse_mode="HTML",
        )

        text = text[len(chunk):].lstrip()
