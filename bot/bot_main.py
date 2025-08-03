import logging
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
import aiohttp
import re
import os
from datetime import datetime
from google.cloud import storage
import uuid
from ml_model import classify_drug_text
from extract_words import extract_drug_words

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot with token
try:
    bot = AsyncTeleBot('YOUR_TELEGRAM_BOT_TOKEN', parse_mode='HTML')
    bot_info = asyncio.run(bot.get_me())
    logger.info(f"Bot initialized successfully. Bot Username: @{bot_info.username}, Bot ID: {bot_info.id}")
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}")
    raise

# Google Cloud Storage setup
GCS_BUCKET_NAME = "your-gcs-bucket-name"
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

SEARCH_QUEUE_FILE = "search_queue.txt"
TARGET_CHANNEL = "YourTargetChannel"
TARGET_CHANNEL_ID = -1001234567890

# Predefined drug-related keywords
DRUG_KEYWORDS = [ ... ]  # (Copy the full keyword list here)

def extract_drug_words_from_message(message):
    if not message:
        return []
    message = message.lower()
    words = re.findall(r'\b\w+\b', message)
    drug_words = [word for word in words if word in DRUG_KEYWORDS]
    return sorted(list(set(drug_words)))

async def upload_image_to_gcs(image_path, image_name):
    try:
        blob = bucket.blob(f"images/{image_name}")
        blob.upload_from_filename(image_path)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        logger.error(f"Error uploading image to GCS: {e}")
        return None

async def get_chat_photo(chat_id):
    try:
        url = f"https://api.telegram.org/bot{bot.token}/getChat"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch chat info: {response.status}")
                    return None
                data = await response.json()
                if not data.get("ok"):
                    logger.error(f"Telegram API error: {data.get('description')}")
                    return None
                photo = data.get("result", {}).get("photo", {})
                file_id = photo.get("big_file_id")
                if not file_id:
                    logger.info("No profile picture found for this chat")
                    return None

                file_url = f"https://api.telegram.org/bot{bot.token}/getFile"
                params = {"file_id": file_id}
                async with session.get(file_url, params=params) as file_response:
                    if file_response.status != 200:
                        logger.error(f"Failed to fetch file info: {file_response.status}")
                        return None
                    file_data = await file_response.json()
                    file_path = file_data["result"]["file_path"]

                download_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
                image_name = f"{chat_id}_{uuid.uuid4()}.jpg"
                temp_image_path = f"temp_{image_name}"

                async with session.get(download_url) as download_response:
                    if download_response.status != 200:
                        logger.error(f"Failed to download image: {download_response.status}")
                        return None
                    with open(temp_image_path, 'wb') as f:
                        f.write(await download_response.read())

                image_url = await upload_image_to_gcs(temp_image_path, image_name)
                os.remove(temp_image_path)
                return image_url
    except Exception as e:
        logger.error(f"Error fetching chat photo: {e}")
        return None

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(
        message,
        "Welcome to the Drug Trace Bot!\n\n"
        "Use /check <channel_username> to scan a channel.\n"
        "Example: /check @channelname"
    )

@bot.message_handler(commands=['check'])
async def check_channel(message):
    # (Same as your PDF — copy the full code logic here)
    pass

@bot.message_handler(content_types=['text'])
async def handle_channel_messages(message):
    # (Same as your PDF — copy the full code logic here)
    pass

async def main():
    logger.info("Bot is starting polling...")
    try:
        await bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"Error in polling: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
