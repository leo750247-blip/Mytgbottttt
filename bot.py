import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Берем токен из переменных окружения Railway
BOT_TOKEN = os.getenv("8969725825:AAHlWpcdAPq034Cx2VVs4PWVMjmOB0iNJVk")

# Временное хранилище балансов (позже перенесем в БД или Google Таблицу)
USER_BALANCES = {123456789: 250.00}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💰 Показать баланс", callback_data="show_balance")]]
    await update.message.reply_text("Привет! Это бот твоей F1-лиги. Нажми кнопку:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    balance = USER_BALANCES.get(user_id, 0.00)
    
    keyboard = [[InlineKeyboardButton("🔄 Обновить", callback_data="show_balance")]]
    await query.edit_message_text(f"💰 Ваш баланс: {balance:.2f} млн.", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: Укажи BOT_TOKEN в переменных окружения Railway!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.run_polling()
