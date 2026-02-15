
import os
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PAPERLESS_API_URL = os.getenv("PAPERLESS_API_URL", "http://webserver:8000/api")
PAPERLESS_API_TOKEN = os.getenv("PAPERLESS_API_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="MedicalVault Bot Online! Use /search <query> to find documents.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a search query. Example: /search x-quang")
        return

    headers = {
        "Authorization": f"Token {PAPERLESS_API_TOKEN}"
    }
    
    try:
        response = requests.get(f"{PAPERLESS_API_URL}/documents/?query={query}", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        if not results:
             await context.bot.send_message(chat_id=update.effective_chat.id, text="No documents found.")
             return

        message = f"Found {data.get('count', 0)} documents:\n"
        for i, doc in enumerate(results[:5]): # Limit to 5 results
            message += f"{i+1}. {doc['title']} (ID: {doc['id']})\n"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except Exception as e:
        logging.error(f"Error searching documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error searching documents.")

async def recent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        "Authorization": f"Token {PAPERLESS_API_TOKEN}"
    }
    
    try:
        response = requests.get(f"{PAPERLESS_API_URL}/documents/?ordering=-created", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        if not results:
             await context.bot.send_message(chat_id=update.effective_chat.id, text="No documents found.")
             return

        message = f"Recent 5 documents:\n"
        for i, doc in enumerate(results[:5]):
            message += f"{i+1}. {doc['title']} (ID: {doc['id']})\n"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except Exception as e:
        logging.error(f"Error getting recent documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error getting recent documents.")

if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set.")
        exit(1)
        
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    search_handler = CommandHandler('search', search)
    recent_handler = CommandHandler('recent', recent)
    
    application.add_handler(start_handler)
    application.add_handler(search_handler)
    application.add_handler(recent_handler)
    
    print("Bot is polling...")
    application.run_polling()
