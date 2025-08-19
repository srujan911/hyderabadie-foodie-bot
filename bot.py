import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from database import find_restaurants

# Load environment variables from .env file
load_dotenv()

# Get the token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Define the states for our conversation
(
    AWAITING_CUISINE,
    AWAITING_LOCATION,
    AWAITING_VEG,
    AWAITING_PRICE,
    AWAITING_RATING,
) = range(5)


# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    welcome_text = (
        "Salaam! I'm the Hyderabadi Foodie Bot. \n\n"
        "I can help you find the best restaurants in Hyderabad. \n\n"
        "To start a search, just type /find."
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_text
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends instructions when the /help command is issued."""
    help_text = (
        "Here's how to use me:\n\n"
        "/start - Shows the welcome message.\n"
        "/find - Starts a new restaurant search.\n"
        "/help - Shows this help message.\n"
        "/cancel - Cancels the current search."
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="No problem! The search has been cancelled.",
    )
    return ConversationHandler.END


# --- Conversation Functions ---
async def find_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the restaurant finding conversation."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Right choice! Chalo miya, em thintavo cheppu? What cuisine are you looking for?",
    )
    return AWAITING_CUISINE


async def received_cuisine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the cuisine input from the user."""
    user_cuisine = update.message.text
    context.user_data["cuisine"] = user_cuisine
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Got it, {user_cuisine}! Now, which area are you looking in?",
    )
    return AWAITING_LOCATION


async def received_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the location input from the user."""
    user_location = update.message.text
    context.user_data["location"] = user_location
    keyboard = [
        [InlineKeyboardButton("🥕 Pure Veg", callback_data="veg_true")],
        [InlineKeyboardButton("🍗 Non-Veg", callback_data="veg_false")],
        [InlineKeyboardButton("Both Are Fine", callback_data="veg_none")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Got it, {user_location}. Now, should I look for Pure Veg, Non-Veg, or are both okay?",
        reply_markup=reply_markup,
    )
    return AWAITING_VEG


async def received_veg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the veg/non-veg preference from the user."""
    query = update.callback_query
    await query.answer()
    context.user_data["veg_preference"] = query.data

    # Provide feedback on the selection
    selected_veg = "Pure Veg" if "true" in query.data else "Non-Veg" if "false" in query.data else "Both"
    await query.edit_message_text(text=f"Selected: {selected_veg}")

    keyboard = [
        [InlineKeyboardButton("₹ Light", callback_data="₹ Light")],
        [InlineKeyboardButton("₹₹ Theek Thaak", callback_data="₹₹ Theek Thaak")],
        [InlineKeyboardButton("₹₹₹ Full Posh", callback_data="any")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Noted. And what's your budget?",
        reply_markup=reply_markup,
    )
    return AWAITING_PRICE


async def received_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the price range preference from the user."""
    query = update.callback_query
    await query.answer()
    context.user_data["price"] = query.data

    # Provide feedback on the selection
    await query.edit_message_text(text=f"Selected: {query.data}")

    keyboard = [
        [InlineKeyboardButton("★★★★☆ & Up", callback_data="4")],
        [InlineKeyboardButton("★★★☆☆ & Up", callback_data="3")],
        [InlineKeyboardButton("Any Rating", callback_data="any")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Almost done! Lastly, should the place have high ratings?",
        reply_markup=reply_markup,
    )
    return AWAITING_RATING


async def received_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the rating preference and initiates the search."""
    query = update.callback_query
    await query.answer()
    context.user_data["rating"] = query.data

    # Provide feedback on the selection
    selected_rating = "★★★★☆ & Up" if "4" in query.data else "★★★☆☆ & Up" if "3" in query.data else "Any Rating"
    await query.edit_message_text(text=f"Selected: {selected_rating}")

    # --- Gather Data and Search ---
    cuisine = context.user_data.get("cuisine")
    location = context.user_data.get("location")
    veg_preference = context.user_data.get("veg_preference")
    price_range = context.user_data.get("price")
    rating_pref = context.user_data.get("rating")

    is_veg = None
    if "true" in veg_preference:
        is_veg = True
    elif "false" in veg_preference:
        is_veg = False

    rating = None
    if rating_pref != "any":
        rating = int(rating_pref)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Got it! Let me find the best spots for you...",
    )

    found_restaurants = find_restaurants(
        cuisine=cuisine,
        location=location,
        is_veg=is_veg,
        price_range=price_range,
        rating=rating,
    )

    # --- Display Results as Photo Cards ---
    if found_restaurants:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Here are the places I found for you:",
        )
        for r in found_restaurants:
            caption = (
                f"*{r['name']}* ({r['location']})\n"
                f"Rating: {r['rating']} ★ | Price: {r['price_range']}"
            )
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Get Directions",
                        url=f"https://www.google.com/maps/search/?api=1&query={r['name'].replace(' ', '+')}+{r['location']}",
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=r["photo_url"],
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I couldn't find any places that match all your criteria.",
        )

    return ConversationHandler.END


# --- Main Application Setup ---
if __name__ == "__main__":
    # Token check
    if not TELEGRAM_TOKEN:
        logging.error("TELEGRAM_TOKEN is not set in the environment variables.")
    else:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        # Conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("find", find_start)],
            states={
                AWAITING_CUISINE: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, received_cuisine
                    )
                ],
                AWAITING_LOCATION: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, received_location
                    )
                ],
                AWAITING_VEG: [CallbackQueryHandler(received_veg)],
                AWAITING_PRICE: [CallbackQueryHandler(received_price)],
                AWAITING_RATING: [CallbackQueryHandler(received_rating)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(conv_handler)

        print("Bot is running...")
        application.run_polling()
