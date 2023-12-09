# Alibaba Telegram Bot

This Telegram bot is designed to parse pictures of products from a given Alibaba link. Users can provide an Alibaba.com web link, and the bot will fetch and send the associated pictures.

## Getting Started

Follow the steps below to set up and run the bot:

### Prerequisites

- Docker

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/andreypomortsev/alibaba_pic_parser.git
    ```

2. Navigate to the project directory:

    ```bash
    cd alibaba_pic_parser
    ```

### Configuration

1. Create a new `.env` file in the project directory:

    ```plaintext
    TOKEN=your_telegram_bot_token
    ```

    Replace `your_telegram_bot_token` with the actual token for your Telegram bot.

### Building the Docker Image

Build the Docker image with improved security:

```bash
docker build --build-arg TOKEN=$TOKEN -t alibaba-bot .
```
### Run the Docker Image

Run the Docker container securely:
```
docker run -it --rm --env-file .env alibaba-bot
```
