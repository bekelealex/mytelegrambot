#  Premium English Mastery Telegram Bot

[![GitHub Actions Status](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/workflows/English%20Mastery%20Bot/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions)

## 📚 About
A professional Telegram bot with **100 advanced English questions** covering all major grammar topics with detailed explanations.

##  Features
- ✅ **100 Expert-Level Questions**
- ✅ **8 Comprehensive Categories**
- ✅ **Detailed Explanations** with grammar rules
- ✅ **Progress Tracking** with visual progress bar
- ✅ **Level-Based Feedback** (Grand Master to Developing)
- ✅ **24/7 Availability** on GitHub Actions

## 📖 Question Categories
| Category | Questions | Topics |
|----------|-----------|--------|
| Reading Passage Completion | 15 | All tenses in context |
| Modal Auxiliaries | 10 | Natural conversations |
| All Conditionals | 15 | Zero to mixed, inverted |
| Reported Speech | 10 | Statements, questions, commands |
| Advanced Vocabulary | 15 | Academic & professional |
| Reading Comprehension | 25 | Complex texts |
| All Tenses Mastery | 10 | Complete tense usage |

## Deployment

### Prerequisites
1. Telegram Bot Token from [@BotFather](https://t.me/botfather)
2. GitHub Account

### Deploy on GitHub Actions (Free)

1. **Fork this repository**

2. **Add your Bot Token to GitHub Secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Add new secret: `BOT_TOKEN` = your token from BotFather

3. **Push to main branch** - bot automatically starts!

### Test Locally
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/english-bot.git
cd english-bot

# Install dependencies
pip install -r requirements.txt

# Set token (Linux/Mac)
export BOT_TOKEN="your_token_here"

# Set token (Windows)
set BOT_TOKEN="your_token_here"

# Run bot
python bot.py
