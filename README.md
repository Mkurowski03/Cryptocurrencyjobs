# Cryptocurrency Jobs Notifier

## Overview

This Python script monitors the Cryptocurrency Jobs website for new listings and sends alerts via Telegram. It automates the process of checking for new job listings every 5 minutes, formats the details, and sends a notification if new jobs are found.

## Features

- **Web Scraping**: Automatically scrapes job listings from a specified cryptocurrency job board.
- **Notifications**: Sends alerts via Telegram for new job listings.
- **Automatic Updates**: Continuously checks for new postings at regular intervals.

## Setup Instructions

### Prerequisites

Ensure Python is installed along with the following libraries:
- `requests`
- `beautifulsoup4`
- `pandas`

Install them using pip:

```bash
pip install requests beautifulsoup4 pandas
```

### Telegram Bot Setup
1. **Create a Telegram Bot**:
   - Talk to BotFather on Telegram to create a new bot and receive your `TELEGRAM_BOT_TOKEN`.
2. **Get Your Chat ID**:
   - Start a conversation with your bot and retrieve your `TELEGRAM_CHAT_ID` from `https://api.telegram.org/bot<YourBOTToken>/getUpdates`.

2. **Set API Token and Chat ID**:
- Open the script in a text editor.
- Replace `#Your telegram bot ID` with your actual `TELEGRAM_BOT_TOKEN`.
- Replace `#Your telegram chat ID` with your `TELEGRAM_CHAT_ID`.

## Additional Information
- The script delays for 5 minutes between checks, which can be adjusted by modifying the `time.sleep(300)` line in the script.
- Ensure the bot has permissions to send messages in your Telegram chat.

For further assistance or to report issues, refer to the script documentation or open an issue in this repository.
