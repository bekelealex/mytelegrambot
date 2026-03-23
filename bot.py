# -*- coding: utf-8 -*-
import logging
import os
import sys
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Setup Logging (Essential for debugging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN') # Ensure this is set in your environment

# 3. Database (Shortened for brevity - keep your full list here)
questions = [
    {
        "id": 0,
        "question": "Read the passage and choose the correct verb form:\n\n'The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.'",
        "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
        "answer": "A",
        "explanation": "Past Perfect Passive 'had been hidden' is used because the hiding occurred before the discovery in 2019."
    },
    # ... Add all 100 questions here following this dictionary format
]

# 4. Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the first question when /start is typed."""
    await send_question(update, context, 0)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, q_index: int):
    """Refactored function to send a question by index."""
    if q_index >= len(questions):
        await update.effective_message.reply_text("🎉 You have completed all questions!")
        return

    q = questions[q_index]
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans_{q_index}_{opt[0]}")] 
        for opt in q["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if this is a new message or an edit
    if update.callback_query:
        await update.callback_query.edit_message_text(text=q["question"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=q["question"], reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button clicks, shows explanations, and moves to next question."""
    query = update.callback_query
    await query.answer() # Removes the "loading" circle on the button
    
    # Data format: ans_INDEX_CHOICE
    data = query.data.split("_")
    q_index = int(data[1])
    user_choice = data[2]
    
    q = questions[q_index]
    is_correct = user_choice == q["answer"]
    
    result_text = "✅ Correct!" if is_correct else f"❌ Incorrect. The answer was {q['answer']}."
    full_response = f"{result_text}\n\n📖 *Explanation:*\n{q['explanation']}\n\n_Loading next question..._"

    # Show explanation briefly
    await query.edit_message_text(text=full_response, parse_mode="Markdown")
    
    # Wait 3 seconds so they can read the explanation, then show next question
    await asyncio.sleep(3)
    await send_question(update, context, q_index + 1)

# 5. Main Execution
def main():
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found!")
        return

    # Build the application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))

    logger.info("🚀 Bot is starting...")
    
    # Use run_polling() - it handles the event loop and "keep alive" automatically
    application.run_polling()

if __name__ == '__main__':
    main()
