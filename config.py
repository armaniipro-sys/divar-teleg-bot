
"""Central place for environment-driven configuration and constants."""
import os

DIVAR_SEARCH_URL = "https://api.divar.ir/v8/postlist/w/search"
DIVAR_POST_DETAIL_URL = "https://api.divar.ir/v8/posts-v2/web/{token}"

DIVAR_CONTACT_URL = os.environ.get(
    "DIVAR_CONTACT_URL",
    "https://api.divar.ir/v8/postcontact/web/contact_info/{token}",
)


def _required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError("{} must be set to a non-empty value.".format(name))
    return value


BOT_TOKEN = _required_env("BOT_TOKEN")
BOT_CHATID = _required_env("BOT_CHATID")

# Check every 10 minutes
SLEEP_SEC = os.environ.get("SLEEP_SEC", "600")

# Fardis - city ID must be verified
SEARCH_CITY_IDS = ["897"]

SEARCH_CATEGORY = "real-estate"

PROXY_URL = os.environ.get("PROXY_URL") or None

DEBUG_DUMP_SECTIONS = os.environ.get("DEBUG_DUMP_SECTIONS", "") == "1"

REQUEST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "referrer": "https://divar.ir/",
    "x-render-type": "CSR",
    "x-standard-divar-error": "true",
}

FOOTER_TEXT = (
    "\n\n"
    "گروه املاک آرمان\n"
    "تلفن تماس: 09121076323"
)
