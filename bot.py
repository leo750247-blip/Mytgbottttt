import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8969725825:AAHlWpcdAPq034Cx2VVs4PWVMjm0B0iNJVk"

USER_BALANCES = {
    123456789: 250.00,
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💰 Показать баланс", callback_data="show_balance")]]
    await update.message.reply_text("Привет! Нажми кнопку:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    balance = USER_BALANCES.get(user_id, 0.00)
    keyboard = [[InlineKeyboardButton("🔄 Обновить", callback_data="show_balance")]]
    await query.edit_message_text(f"💰 Ваш баланс: {balance:.2f} ₽", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
