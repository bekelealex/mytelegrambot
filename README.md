# 🏆 Premium English Mastery Telegram Bot

[![Deploy on Render](https://img.shields.io/badge/Deploy%20on-Render-blue?logo=render)](https://render.com/deploy)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-green.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots)

## 📚 About

A professional Telegram bot with **100 advanced English questions** covering all major grammar topics with detailed explanations and ultra-fast responses.

## ✨ Features

- ✅ **100 Expert-Level Questions**
- ✅ **8 Comprehensive Categories**
- ✅ **Ultra-Fast Responses** (<100ms)
- ✅ **Auto-Clearing Explanations** (1 second)
- ✅ **Progress Tracking** with visual bar
- ✅ **User Preferences** (toggle explanations)
- ✅ **Global Statistics**
- ✅ **Scalable Production Architecture**

## 🚀 Categories

| Category | Questions |
|----------|-----------|
| Reading Passage Completion | 15 |
| Modal Auxiliaries | 10 |
| All Conditionals | 15 |
| Reported Speech | 10 |
| Advanced Vocabulary | 15 |
| Reading Comprehension | 25 |
| All Tenses | 10 |

## 🎯 Quick Start

### 1. Create Bot on Telegram
- Message [@BotFather](https://t.me/botfather)
- Send `/newbot` and follow instructions
- Copy your bot token

### 2. Deploy on Render (Free)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Or manually:

1. Fork this repository
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Add environment variables:
   - `BOT_TOKEN`: Your bot token
   - `ENVIRONMENT`: `production`
   - `WEBHOOK_URL`: Your Render URL (e.g., `https://your-bot.onrender.com`)
6. Click "Create Web Service"

### 3. Test Your Bot
- Open Telegram
- Search for your bot
- Send `/start`

## 📊 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the quiz |
| `/stats` | View global statistics |

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/your-username/english-mastery-bot.git
cd english-mastery-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN="your_token_here"

# Run bot
python bot.py
