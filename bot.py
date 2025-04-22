import os, time, requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Lee el token de las variables de entorno
BOT_TOKEN = os.getenv("Zero_bot")
bot = Bot(token=BOT_TOKEN)

# Variable global para chat_id
chat_id = None

def start(update, context):
    global chat_id
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id,
        text="¡Hola! Soy Jkaii_bot, tu asistente de inversiones.")

def check_tokens():
    DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/bsc"
    try:
        data = requests.get(DEX_URL).json().get("pairs", [])
        # Aquí iría la lógica de filtrado...
        # Si encuentra tokens, usa bot.send_message(chat_id, mensaje)
    except:
        pass

if name == "main":
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    while True:
        check_tokens()
        time.sleep(60)
