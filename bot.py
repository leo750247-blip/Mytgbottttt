import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = "8969725825:AAHlWpcdAPq034Cx2VVs4PWVMjm0B0iNJVk"

USER_BALANCES = {
    123456789: 250.00,
}

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("💰 Показать баланс", callback_data="show_balance")]]
    update.message.reply_text("Привет! Нажми кнопку:", reply_markup=InlineKeyboardMarkup(keyboard))

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    balance = USER_BALANCES.get(user_id, 0.00)
    keyboard = [[InlineKeyboardButton("🔄 Обновить", callback_data="show_balance")]]
    query.edit_message_text(f"💰 Ваш баланс: {balance:.2f} ₽", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
