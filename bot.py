# -*- coding: utf-8 -*-
"""
Premium English Mastery Telegram Bot
PRODUCTION GRADE - Webhook Mode | Ultra Fast | Scalable
"""

import logging
import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.constants import ParseMode

# ==================== CONFIGURATION ====================

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-domain.com')
PORT = int(os.getenv('PORT', 8000))
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN not found!")
    sys.exit(1)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==================== DATA STRUCTURES ====================

# Store user sessions in memory (fast)
user_sessions: Dict[int, dict] = {}

# Store user preferences
user_preferences: Dict[int, dict] = {}

# Stats tracking
stats = {
    "total_users": 0,
    "total_questions_answered": 0,
    "total_correct": 0,
    "active_sessions": 0,
    "start_time": datetime.now().isoformat()
}

# ==================== QUESTIONS DATABASE ====================
# Load questions from JSON file (better for production)
# For now, using the full 100 questions from previous version
# In production, load from a separate file

def load_questions():
    """Load questions from JSON file (more scalable)"""
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("questions.json not found, using default questions")
        return get_default_questions()

def get_default_questions():
    """Return default questions (same as previous version)"""
    # Placeholder for your 100 questions
    # In production, keep your complete 100 questions here
    return [
        {
            "question": "Read the passage and choose the correct verb form:\n\n'The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.'",
            "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
            "answer": "A",
            "explanation": "Past Perfect Passive 'had been hidden' is used because the hiding occurred before the discovery in 2019."
        }
        # ... Add your full 100 questions here
    ]

questions = load_questions()

# ==================== CACHE FOR FAST ACCESS ====================
# Pre-calculate question counts and categories for faster responses
TOTAL_QUESTIONS = len(questions)
QUESTION_CATEGORIES = {}

for idx, q in enumerate(questions):
    if idx < 15:
        category = "📖 Reading Completion"
    elif idx < 25:
        category = "💬 Modal Conversations"
    elif idx < 40:
        category = "🔄 Conditionals"
    elif idx < 50:
        category = "🗣️ Reported Speech"
    elif idx < 65:
        category = "📚 Advanced Vocabulary"
    elif idx < 90:
        category = "📖 Reading Comprehension"
    else:
        category = "⏰ Tense Mastery"
    QUESTION_CATEGORIES[idx] = category

# ==================== HELPER FUNCTIONS ====================

def get_level(percentage: float) -> tuple:
    """Return achievement level based on percentage"""
    if percentage >= 95:
        return ("🏆 GRAND MASTER", "🌟 LEGENDARY! You're in the top 1% of English masters!")
    elif percentage >= 85:
        return ("🥇 ADVANCED EXPERT", "🎉 EXCELLENT! You've demonstrated superior mastery!")
    elif percentage >= 75:
        return ("🥈 PROFICIENT", "📚 VERY GOOD! You have strong command of advanced English!")
    elif percentage >= 65:
        return ("🥉 COMPETENT", "💪 GOOD EFFORT! You have solid skills!")
    elif percentage >= 50:
        return ("📘 INTERMEDIATE", "📖 KEEP PRACTICING! You're building a strong foundation!")
    else:
        return ("🌱 DEVELOPING", "🌟 EVERY MASTER WAS ONCE A BEGINNER! Review and try again!")

def get_progress_bar(current: int, total: int, width: int = 10) -> str:
    """Generate progress bar"""
    filled = int((current / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_category(index: int) -> str:
    """Get category for question index"""
    return QUESTION_CATEGORIES.get(index, "📚 English Mastery")

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    # Initialize user session
    user_sessions[user_id] = {
        "index": 0,
        "score": 0,
        "questions_answered": 0,
        "start_time": datetime.now().isoformat()
    }
    
    # Initialize preferences
    if user_id not in user_preferences:
        user_preferences[user_id] = {"show_explanations": True}
    
    # Update stats
    if user_id not in stats.get("users", set()):
        stats["total_users"] += 1
        if "users" not in stats:
            stats["users"] = set()
        stats["users"].add(user_id)
    
    logger.info(f"📱 User {username} ({user_id}) started the bot")
    
    # Create settings button
    settings_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")]
    ])
    
    show_exp = user_preferences[user_id].get("show_explanations", True)
    
    await update.message.reply_text(
        f"<b>🏆 PREMIUM ENGLISH MASTERY SUITE</b>\n\n"
        f"<b>📚 {TOTAL_QUESTIONS} Expert-Level Questions:</b>\n"
        f"✓ Reading Passage Completion\n"
        f"✓ Modal Auxiliaries\n"
        f"✓ All Conditionals\n"
        f"✓ Reported Speech\n"
        f"✓ Advanced Vocabulary\n"
        f"✓ Reading Comprehension\n"
        f"✓ All Tenses\n\n"
        f"<b>⚙️ Settings:</b>\n"
        f"• Explanations: {'✅ ON' if show_exp else '❌ OFF'}\n\n"
        f"<b>🚀 Production Features:</b>\n"
        f"✓ Webhook mode (instant responses)\n"
        f"✓ Non-blocking operations\n"
        f"✓ Scalable architecture\n\n"
        f"<b>🎯 Type /stats to see global stats!</b>",
        reply_markup=settings_button,
        parse_mode=ParseMode.HTML
    )
    await send_question(update, context)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show global statistics"""
    user_id = update.effective_user.id
    
    # Admin check (optional - add your user ID)
    # ADMIN_IDS = [123456789]  # Your Telegram ID
    # if user_id not in ADMIN_IDS:
    #     await update.message.reply_text("🔒 This command is for admins only")
    #     return
    
    total_answered = stats.get("total_questions_answered", 0)
    total_correct = stats.get("total_correct", 0)
    accuracy = (total_correct / total_answered * 100) if total_answered > 0 else 0
    
    stats_text = (
        f"<b>📊 GLOBAL STATISTICS</b>\n\n"
        f"👥 Total Users: {stats['total_users']}\n"
        f"📝 Questions Answered: {total_answered:,}\n"
        f"✅ Correct Answers: {total_correct:,}\n"
        f"📈 Global Accuracy: {accuracy:.1f}%\n"
        f"🟢 Active Sessions: {len(user_sessions)}\n"
        f"🚀 Started: {stats['start_time']}\n\n"
        f"<i>Type /start to begin your journey!</i>"
    )
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.HTML)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current question"""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or session["index"] >= TOTAL_QUESTIONS:
        # Quiz completed
        score = session.get("score", 0) if session else 0
        percentage = (score / TOTAL_QUESTIONS) * 100
        level, feedback = get_level(percentage)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"<b>🏆 QUIZ COMPLETE!</b>\n\n"
                 f"📊 <b>Final Score:</b> {score}/{TOTAL_QUESTIONS}\n"
                 f"📈 <b>Percentage:</b> {percentage:.1f}%\n"
                 f"⭐ <b>Level:</b> {level}\n\n"
                 f"{feedback}\n\n"
                 f"<i>Type /start to challenge yourself again! 🔄</i>",
            parse_mode=ParseMode.HTML
        )
        return
    
    idx = session["index"]
    q = questions[idx]
    
    # Create keyboard
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Progress bar
    progress = get_progress_bar(idx, TOTAL_QUESTIONS)
    percent = (idx / TOTAL_QUESTIONS) * 100
    category = get_category(idx)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"<b>{category}</b>\n"
             f"<b>📝 Question {idx + 1}/{TOTAL_QUESTIONS}</b>\n"
             f"<code>[{progress}]</code> <i>{percent:.0f}% Complete</i>\n\n"
             f"{q['question']}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks with ULTRA FAST response"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # INSTANT acknowledgment
    await query.answer()
    
    # Handle settings menu
    if query.data == "open_settings":
        await show_settings(update, context)
        return
    elif query.data == "toggle_explanations":
        await toggle_explanations(update, context)
        return
    elif query.data == "view_stats":
        await view_user_stats(update, context)
        return
    elif query.data == "back_to_quiz":
        await back_to_quiz(update, context)
        return
    
    # Handle quiz answers
    session = user_sessions.get(user_id)
    if not session:
        return
    
    idx = session["index"]
    if idx >= TOTAL_QUESTIONS:
        return
    
    user_choice = query.data
    q = questions[idx]
    
    # Disable buttons immediately (prevents double clicks)
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except:
        pass
    
    # Update stats
    stats["total_questions_answered"] = stats.get("total_questions_answered", 0) + 1
    
    # Check answer
    if user_choice == q["answer"]:
        session["score"] += 1
        stats["total_correct"] = stats.get("total_correct", 0) + 1
        result_text = "✅ <b>CORRECT!</b> 🎯\n\n"
    else:
        correct_letter = q["answer"]
        correct_text = next(opt for opt in q["options"] if opt.startswith(correct_letter))
        result_text = f"❌ <b>INCORRECT</b>\n\n<b>✓ Correct Answer:</b> {correct_text}\n\n"
    
    # Get user preference for explanations
    show_explanations = user_preferences.get(user_id, {}).get("show_explanations", True)
    
    if show_explanations:
        explanation_text = result_text + f"<b>📖 Explanation:</b>\n{q['explanation']}\n\n<i>⚡ Next question in 1 second...</i>"
    else:
        explanation_text = result_text + f"<i>⚡ Next question in 1 second...</i>"
    
    # Send explanation
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=explanation_text,
        parse_mode=ParseMode.HTML
    )
    
    # Move to next question IMMEDIATELY
    session["index"] += 1
    session["questions_answered"] = session.get("questions_answered", 0) + 1
    
    # Send next question (non-blocking)
    asyncio.create_task(send_question(update, context))
    
    # Delete explanation after 1 second (only if explanations are on)
    if show_explanations:
        async def delete_later():
            await asyncio.sleep(1)
            try:
                await msg.delete()
            except:
                pass
        asyncio.create_task(delete_later())

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    query = update.callback_query
    user_id = query.from_user.id
    
    show_exp = user_preferences.get(user_id, {}).get("show_explanations", True)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"{'✅' if show_exp else '❌'} Show Explanations",
            callback_data="toggle_explanations"
        )],
        [InlineKeyboardButton(
            "📊 My Statistics",
            callback_data="view_stats"
        )],
        [InlineKeyboardButton(
            "🔙 Back to Quiz",
            callback_data="back_to_quiz"
        )]
    ])
    
    await query.edit_message_text(
        text=f"<b>⚙️ Settings</b>\n\n"
             f"<b>Explanations:</b> {'ON - You see detailed explanations' if show_exp else 'OFF - Only correct/incorrect'}\n\n"
             f"<b>Tips:</b>\n"
             f"• OFF = faster quiz (1 sec per question)\n"
             f"• ON = detailed learning (1 sec explanation)\n\n"
             f"<i>Choose your preference below:</i>",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await query.answer()

async def toggle_explanations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle explanation visibility"""
    query = update.callback_query
    user_id = query.from_user.id
    
    current = user_preferences.get(user_id, {}).get("show_explanations", True)
    user_preferences[user_id] = {"show_explanations": not current}
    
    await query.answer(f"Explanations turned {'ON' if not current else 'OFF'}!")
    await show_settings(update, context)

async def view_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    query = update.callback_query
    user_id = query.from_user.id
    
    session = user_sessions.get(user_id, {})
    idx = session.get("index", 0)
    score = session.get("score", 0)
    questions_answered = session.get("questions_answered", 0)
    
    if questions_answered > 0:
        accuracy = (score / questions_answered) * 100
        stats_text = (
            f"<b>📊 Your Statistics</b>\n\n"
            f"📝 Completed: {idx}/{TOTAL_QUESTIONS}\n"
            f"✅ Correct: {score}\n"
            f"📈 Accuracy: {accuracy:.1f}%\n"
            f"🎯 Remaining: {TOTAL_QUESTIONS - idx}\n\n"
            f"⚙️ Explanations: {'ON' if user_preferences.get(user_id, {}).get('show_explanations', True) else 'OFF'}\n\n"
            f"<i>Keep going! You're making progress!</i>"
        )
    else:
        stats_text = (
            f"<b>📊 Your Statistics</b>\n\n"
            f"📝 No questions completed yet!\n"
            f"Start the quiz to see your stats.\n\n"
            f"⚙️ Explanations: {'ON' if user_preferences.get(user_id, {}).get('show_explanations', True) else 'OFF'}"
        )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="open_settings")]
    ])
    
    await query.edit_message_text(
        text=stats_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await query.answer()

async def back_to_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to current question"""
    query = update.callback_query
    user_id = query.from_user.id
    
    session = user_sessions.get(user_id)
    
    if session and session["index"] < TOTAL_QUESTIONS:
        idx = session["index"]
        q = questions[idx]
        
        keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        progress = get_progress_bar(idx, TOTAL_QUESTIONS)
        percent = (idx / TOTAL_QUESTIONS) * 100
        category = get_category(idx)
        
        await query.edit_message_text(
            text=f"<b>{category}</b>\n"
                 f"<b>📝 Question {idx + 1}/{TOTAL_QUESTIONS}</b>\n"
                 f"<code>[{progress}]</code> <i>{percent:.0f}% Complete</i>\n\n"
                 f"{q['question']}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    else:
        await query.edit_message_text("Quiz completed! Type /start to begin again!")
    
    await query.answer()

# ==================== ERROR HANDLER ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    try:
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ An error occurred. Please try again or type /start to restart."
            )
    except:
        pass

# ==================== MAIN ====================

def main():
    """Main function - Production ready with webhook support"""
    
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)
    
    # In production, use webhook
    if ENVIRONMENT == "production":
        logger.info("🚀 Starting bot in PRODUCTION mode with webhook...")
        
        # Set webhook
        webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
        
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=webhook_url
        )
    else:
        # Development mode with polling
        logger.info("🔧 Starting bot in DEVELOPMENT mode with polling...")
        app.run_polling()

if __name__ == "__main__":
    main()
