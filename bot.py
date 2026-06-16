import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Замени на свой токен от @BotFather
BOT_TOKEN = "8969725825:AAHlWpcdAPq034Cx2VVs4PWVMjmOB0iNJVk"

# Фиктивные балансы пользователей (замени на реальную БД)
USER_BALANCES = {
    123456789: 250.00,   # user_id: баланс
}

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Показать баланс", callback_data="show_balance")],
        [InlineKeyboardButton("🔄 Обновить", callback_data="show_balance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Привет! Я бот для проверки баланса.\n\nНажми кнопку ниже:",
        reply_markup=reply_markup,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # убирает "часики" на кнопке

    if query.data == "show_balance":
        user_id = query.from_user.id
        username = query.from_user.first_name

        # Получаем баланс (если нет — показываем 0)
        balance = USER_BALANCES.get(user_id, 0.00)

        keyboard = [
            [InlineKeyboardButton("🔄 Обновить баланс", callback_data="show_balance")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=(
                f"👤 Пользователь: {username}\n"
                f"🆔 ID: {user_id}\n\n"
                f"💰 Ваш баланс: {balance:.2f} ₽\n\n"
                f"_Нажми кнопку для обновления_"
            ),
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
