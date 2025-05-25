import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde .env

# — Telegram —
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No se encontró BOT_TOKEN en .env")

ADMIN_IDS_STR = os.getenv("ADMIN_IDS")
if not ADMIN_IDS_STR:
    raise ValueError("No se encontró ADMIN_IDS en .env")
ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS_STR.split(",")]

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
if not TARGET_CHANNEL_ID:
    raise ValueError("No se encontró TARGET_CHANNEL_ID en .env")

# — Reddit —
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
if not REDDIT_CLIENT_ID:
    raise ValueError("No se encontró REDDIT_CLIENT_ID en .env")

REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
if not REDDIT_CLIENT_SECRET:
    raise ValueError("No se encontró REDDIT_CLIENT_SECRET en .env")

REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
if not REDDIT_USER_AGENT:
    raise ValueError("No se encontró REDDIT_USER_AGENT en .env")

if __name__ == "__main__":
    # Debug rápido
    print("✅ Telegram y Reddit configurados correctamente:")
    print(f"  • BOT_TOKEN: {'*'*5}{BOT_TOKEN[-5:]}")
    print(f"  • ADMIN_IDS: {ADMIN_IDS}")
    print(f"  • TARGET_CHANNEL_ID: {TARGET_CHANNEL_ID}")
    print(f"  • REDDIT_CLIENT_ID: {REDDIT_CLIENT_ID}")
    print(f"  • REDDIT_USER_AGENT: {REDDIT_USER_AGENT}")
