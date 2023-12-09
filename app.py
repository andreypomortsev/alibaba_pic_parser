#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
import requests
from ali_parser import get_list_of_picture_urls

# Load environment variables from the .env file
load_dotenv()

# Get the Telegram bot token from the environment variable
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError(
        "Telegram bot token not provided. Set the TOKEN environment variable."
    )

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Define your handlers using aiogram decorators
@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer(
        "Hello! I'm your bot. Send me an Alibaba.com web link, and I'll fetch and send pictures."
    )


@dp.message_handler(lambda message: message.text.startswith(("http://", "https://")))
async def handle_web_link(message: Message):
    # Get the web link from the user's message
    web_link = message.text

    # Get a list of picture URLs from the provided web link
    picture_urls = get_list_of_picture_urls(web_link)

    if picture_urls:
        # Call photo_saver to download and send back pictures
        await photo_saver(message, picture_urls)
    else:
        await message.answer("No picture URLs found on the provided web link.")


# Update the photo_saver function to use aiogram's send_photo method
async def photo_saver(message: Message, urls: list):
    for name, picture in enumerate(urls):
        # Send a GET request to the image URL
        response = requests.get(picture)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the image content to a local file
            with open(f"image_{name}.jpg", "wb") as file:
                file.write(response.content)

            # Send the image back to the user
            with open(f"image_{name}.jpg", "rb") as photo:
                await bot.send_photo(message.chat.id, photo)

            print(f"Image saved successfully as image_{name}.jpg")
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")
            await message.answer(
                f"Failed to download the image. Status code: {response.status_code}"
            )

def main():
    # Start the Bot
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
