import os
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# API Keys
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Flask (Render အတွက် လိုအပ်တာ)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

# Telegram Bot Logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="မင်္ဂလာပါ။ Manhwa ပုံလေးတွေ ပို့ပေးပါ၊ ကျွန်တော် ဘာသာပြန်ပေးပါမယ်။")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ပုံလေး ရပါပြီ၊ ခဏစောင့်ပေးပါ...")
    # ဒီနေရာမှာ Image Processing နဲ့ Gemini Translation Code တွေကို ဆက်ထည့်ရပါမယ်
    # လောလောဆယ် Test လုပ်ဖို့ စာပြန်ပို့မယ်
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ပုံထဲက စာတွေကို ဘာသာပြန်နေပါပြီ...")

if __name__ == '__main__':
    # Telegram Bot ကို Background မှာ Run မယ်
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Flask ကို Run မယ်
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    application.run_polling()
    
