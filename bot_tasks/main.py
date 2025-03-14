from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import Config, load_config
from lexicon import LEXICON
from work_db import add_task_db, update_task_db, del_task_db, list_db

CHOOSING, TYPING_CHOICE_ADD, TYPING_CHOICE_UPDATE_ID, TYPING_CHOICE_UPDATE_DESCRIPTION, TYPING_CHOICE_DEL = range(5)

#start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_1 = InlineKeyboardButton(
        text='✅ Добавить задачу',
        callback_data='button_pressed1'
    )
    button_2 = InlineKeyboardButton(
        text='🔄 Обновить задачу',
        callback_data='button_pressed2'
    )
    button_3 = InlineKeyboardButton(
        text='❌ Удалить задачу',
        callback_data='button_pressed3'
    )

    button_4 = InlineKeyboardButton(
        text='📒 Показать все задачи',
        callback_data='button_pressed4'
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3], [button_4]]
    )

    user = update.effective_user
    await update.message.reply_html(
        text=f'Привет, {user.first_name}! {LEXICON["/start"]}',
        reply_markup=keyboard
    )

#add
async def add_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки '✅ Добавить задачу'. Далее пользователь отправляет описание задачи"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text="Введи задачу, которую хочешь добавить")
    return TYPING_CHOICE_ADD

async def add_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды '/add'. Далее пользователь отправляет описание задачи"""
    await update.message.reply_text(text="Введи задачу, которую хочешь добавить")
    return TYPING_CHOICE_ADD




#update
async def update_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки '🔄 Обновить задачу'. Далее пользователь отправляет id задачи"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text="Введи id задачи, которую вы хочешь изменить")
    return TYPING_CHOICE_UPDATE_ID

async def update_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды '/update'. Далее пользователь отправляет id задачи"""
    await update.message.reply_text(text="Введи id задачи, которую вы хочешь изменить")
    return TYPING_CHOICE_UPDATE_ID

async def get_task_id_for_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем id задачи для обновления и просим пользователя ввести новое описание задачи"""
    task_id = update.message.text
    context.user_data['task_id'] = task_id  # Сохраняем ID в user_data
    await update.message.reply_text(text="Введи новое описание задачи:")
    return TYPING_CHOICE_UPDATE_DESCRIPTION



#del
async def del_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки '❌ Удалить задачу'. Далее пользователь отправляет id задачи, которую хочет удалить"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text="Введи id задачи, которую хочешь удалить")
    return TYPING_CHOICE_DEL


async def del_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды '/del'. Далее пользователь отправляет id задачи, которую хочет удалить"""
    await update.message.reply_text(text="Введи id задачи, которую хочешь удалить")
    return TYPING_CHOICE_DEL


#list
async def list_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия кнопки '📒 Показать все задачи'. Отправляется список задач по пользователю"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text="Вот, что мне удалось получить:")
    # Вызов list_db
    await list_db(update, context)


async def list_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды '/list'. Отправляется список задач по пользователю"""
    await update.message.reply_text(text="Вот, что мне удалось получить:")
    # Вызов list_db
    await list_db(update, context)


#other_text
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений вне команд"""
    await update.message.reply_text("К сожалению, я не знаю, что ответить. Если у тебя есть какой-либо запрос, попробуй воспользоваться командами через /start")


#done
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение работы с задачами"""
    await update.message.reply_text("Готово")



def main() -> None:
    config: Config = load_config()

    """Старт бота"""
    application = Application.builder().token(config.tg_bot.token).build()

    """Обработчик команды /add или нажатия клавиши '✅ Добавить задачу'"""
    conv_handler_add = ConversationHandler(
        entry_points=[
            CommandHandler("add", add_task_command),
            CallbackQueryHandler(add_task_button, pattern="^button_pressed1$"),
        ],
        states={
            TYPING_CHOICE_ADD: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), add_task_db),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    """Обработчик команды /update или нажатия клавиши '🔄 Обновить задачу'"""
    conv_handler_update = ConversationHandler(
        entry_points=[
            CommandHandler("update", update_task_command),
            CallbackQueryHandler(update_task_button, pattern="^button_pressed2$"),
        ],
        states={
            TYPING_CHOICE_UPDATE_ID: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND & ~filters.Regex("^Done$"),
                    get_task_id_for_update
                ),
            ],
            TYPING_CHOICE_UPDATE_DESCRIPTION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND & ~filters.Regex("^Done$"),
                    update_task_db
                ),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    """Обработчик команды /del или нажатия клавиши '❌ Удалить задачу'"""
    conv_handler_del = ConversationHandler(
        entry_points=[
            CommandHandler("del", del_task_command),
            CallbackQueryHandler(del_task_button, pattern="^button_pressed3$"),
        ],
        states={
            TYPING_CHOICE_DEL: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), del_task_db),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )


    """Обработчик команды /list или нажатия клавиши '📒 Показать все задачи'"""
    conv_handler_list = ConversationHandler(
        entry_points=[
            CommandHandler("list", list_task_command),
            CallbackQueryHandler(list_task_button, pattern="^button_pressed4$"),
        ],
        states={},
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler_add)
    application.add_handler(conv_handler_update)
    application.add_handler(conv_handler_del)
    application.add_handler(conv_handler_list)
    application.add_handler(CommandHandler("start", start))
    # Обработчик для любых текстовых сообщений вне команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
