# Telegram Setup Guide

## Overview

This guide walks you through setting up Telegram integration for SC Chatbot POC.

## Prerequisites

- Python 3.11+
- Internet connection
- Telegram account

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a bot name (must end in "bot" for the username)
4. Copy the bot token provided by @BotFather

## Step 2: Configure Environment Variables

Add the following to your `.env` file:

```env
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional: Production webhook URL
# TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhooks/telegram

# Optional: Webhook verification token
# TELEGRAM_VERIFICATION_TOKEN=your_verification_token
```

## Step 3: Set Up Webhook

You have two options:

### Option A: Polling Mode (POC Recommended)

The webhook handler will use polling mode by default. This is simpler for POC.

### Option B: Webhook Mode (Production)

For production, set up a webhook:

1. **Set webhook URL:**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d 'url=https://your-domain.com/webhooks/telegram'
   ```

2. **Restart the backend:**
   ```bash
   make docker-up
   ```

## Step 4: Test Your Bot

1. **Open Telegram**
2. **Find your bot**
3. **Send `/start`**
4. **Try asking questions**

Example commands:
- `/start` - Initialize the bot
- `/help` - Show help message

## Step 5: Get Chat ID

To get your chat ID:

1. Send `/start` to your bot
2. Use the **Test Webhook** endpoint to test with your chat:
   ```bash
   curl -X POST "http://localhost:8000/webhooks/telegram/test?bot_token=YOUR_TOKEN" \
     -d "chat_id=YOUR_CHAT_ID" \
     -d "message=Hello from SC Chatbot!"
   ```

Or use the `/help` command which returns your chat ID.

## Troubleshooting

### Issue: Bot doesn't respond

**Solution:** Check if the webhook URL is accessible and the bot token is correct.

### Issue: Webhook verification failed

**Solution:** Make sure the webhook URL is publicly accessible (not behind localhost).

### Issue: Messages not delivered

**Solution:** Enable webhook debugging:
```env
DEBUG=True
```

## Next Steps

1. Upload knowledge documents
2. Define custom tools
3. Configure LLM settings

## See Also

- [Getting Started Guide](getting-started.html)
- [Telegram API Documentation](https://core.telegram.org/bots/api)
- [Webhook Handler](../../src/backend/api/webhooks.py)