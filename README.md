# Hyderabadi Foodie Bot

A Telegram bot that helps you find the best restaurants in Hyderabad, tailored to your preferences.

## Features

- **Conversational Search:** Find restaurants based on cuisine, location, price range, and rating through a simple and intuitive conversation.
- **Interactive UI:** Uses inline keyboards for easy selection.
- **Photo Cards:** Displays restaurant results as attractive photo cards with essential details and a link to get directions.
- **Secure:** Uses environment variables to keep your Telegram bot token safe.
- **User-Friendly:** Includes `/start`, `/help`, and `/cancel` commands for a smooth user experience.

## How to Use

1.  **Start a conversation** with the bot on Telegram.
2.  Use the `/find` command to **start a new search**.
3.  **Answer the bot's questions** about your preferences.
4.  **Confirm your selections** and let the bot find the best restaurants for you.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/hyderabadie-foodie-bot.git
    cd hyderabadie-foodie-bot
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create a `.env` file** in the root of the project.
2.  **Add your Telegram bot token** to the `.env` file:
    ```
    TELEGRAM_TOKEN='YOUR_NEW_TOKEN_HERE'
    ```

## Running the Bot

```bash
python bot.py
```
