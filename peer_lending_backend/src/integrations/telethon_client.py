# peer_lending_backend/src/security/telethon_client.py

from telethon import TelegramClient

API_ID = 123456      # your Telegram API ID
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@your_channel_or_chat_id"

client = TelegramClient("peer_lending_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def send_telegram_message(text: str):
    await client.send_message(CHANNEL_ID, text)
