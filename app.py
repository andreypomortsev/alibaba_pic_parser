#!/usr/bin/env python3
"""
This script defines a Telegram bot that fetches and sends pictures from Alibaba.com web links.
"""

import os
from dotenv import load_dotenv
import requests
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, InputFile
from aiogram.utils import executor
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


async def photo_saver(message: Message, urls: list):
    """
    Download and send back pictures to the user.

    Args:
        message (Message): The message from the user.
        urls (list): List of picture URLs to be processed.
    """
    for name, picture in enumerate(urls):
        # Send a GET request to the image URL
        response = requests.get(picture, timeout=2)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the image content to a local file
            with open(f"image_{name}.jpg", "wb") as file:
                file.write(response.content)

            # Send the image back to the user
            with open(f"image_{name}.jpg", "rb") as photo:
                # Use InputFile to send the file as a document
                photo_input = InputFile(photo)
                await bot.send_document(message.chat.id, photo_input)
        else:
            await message.answer(
                f"Failed to download the image. Status code: {response.status_code}"
            )


@dp.message_handler(commands=["start"])
async def start(message: Message):
    """
    Handle the /start command and send a welcome message.

    Args:
        message (Message): The message from the user.
    """
    await message.answer(
        "Hello! I'm your bot. Send me an Alibaba.com web link, and I'll fetch and send pictures."
    )


@dp.message_handler(lambda message: message.text.startswith(("http://", "https://")))
async def handle_web_link(message: Message):
    """
    Handle messages containing web links.

    Args:
        message (Message): The message from the user.
    """
    # Get the web link from the user's message
    web_link = message.text

    # Get a list of picture URLs from the provided web link
    picture_urls = get_list_of_picture_urls(web_link)

    if picture_urls:
        # Call photo_saver to download and send back pictures
        await photo_saver(message, picture_urls)
    else:
        await message.answer("No picture URLs found on the provided web link.")

def main():
    """
    Start the Telegram bot.
    """
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
