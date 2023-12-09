#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_list_of_picture_urls(url: str) -> list:
    """Checks the link on alibaba.com
    and returns a list of jpg files from the given link
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all img tags with a src attribute
        img_tags = soup.find_all("img", src=True)

        # Extract the image URLs
        img_urls = [urljoin(url, img["src"]) for img in img_tags]

        # Filter URLs that end with '.jpg'
        jpg_urls = [img_url for img_url in img_urls if img_url.lower().endswith(".jpg")]

        # Extract unique URLs without duplicates
        picture_urls = list(
            set(
                jpg_url.split("_")[0]
                for jpg_url in jpg_urls
                if jpg_url.split("_")[0].endswith(".jpg")
            )
        )
        return picture_urls

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []
