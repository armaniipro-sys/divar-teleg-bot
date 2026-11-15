
"""Telegram bot setup and message formatting/sending."""

import telegram
import config
from hashtags import generate_hashtags

req_proxy = telegram.request.HTTPXRequest(
    proxy_url=config.PROXY_URL or None,
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
    lines = []

    lines.append(f"🏠 {ad.title}")

    location = ad.posted_in or ad.district
    if location:
        lines.append(f"📍 محل آگهی: {location}")

    price = f"{ad.price:,} تومان" if ad.price else "توافقی"
    lines.append(f"💰 قیمت: {price}")

    if ad.features:
        lines.append("\nمشخصات:")
        for label, value in ad.features:
            lines.append(f"▪️ {label}: {value}")

    if ad.description:
        lines.append(f"\nتوضیحات:\n{ad.description}")

    hashtags = generate_hashtags(ad)
    if hashtags:
        lines.append("\n" + " ".join(f"#{tag}" for tag in hashtags))

    lines.append(config.FOOTER_TEXT)

    return "\n".join(lines)


async def send_telegram_message(ad):
    """Send text first, then images."""

    text = build_message_text(ad)

    # Send text in safe chunks without HTML parsing.
    limit = 4000

    while text:
        chunk = text[:limit]

        if len(text) > limit:
            split_at = chunk.rfind("\n")
            if split_at > 0:
                chunk = chunk[:split_at]

        try:
            await bot.send_message(
                chat_id=config.BOT_CHATID,
                text=chunk,
            )
        except Exception as error:
            print(
                f"TELEGRAM TEXT ERROR: "
                f"{type(error).__name__}: {error}"
            )
            raise

        text = text[len(chunk):].lstrip()

    # Send images separately. Image errors do not cancel text delivery.
    for photo in (ad.images or [])[:10]:
        try:
            await bot.send_photo(
                chat_id=config.BOT_CHATID,
                photo=photo,
            )
        except Exception as error:
            print(
                f"TELEGRAM PHOTO ERROR: "
                f"{type(error).__name__}: {error}"
            )
