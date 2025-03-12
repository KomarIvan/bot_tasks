from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import sqlite3



conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS dialog_db(
        id_task INTEGER Primary Key AUTOINCREMENT,
        id_user_tg INTEGER,
        user_tg TEXT,
        user_first_name TEXT,
        description_task TEXT 
    )
    """
)
conn.commit()
conn.close()


async def add_task_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление задачи с использованием id пользователя, его tg имени, имени в телеграмме и текста задачи"""
    task_text = update.message.text
    user = update.effective_user

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO dialog_db (id_user_tg, user_tg,user_first_name, description_task)
        VALUES (?,?,?,?)
        """, (user.id, user.username, user.first_name, task_text),
    ),
    conn.commit()
    conn.close()
    await update.message.reply_text("Готово, я все записала")
    return ConversationHandler.END



async def update_task_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обновление задачи по id задачи и нового описания"""
    task_description  = update.message.text
    task_id = context.user_data.get('task_id')
    user = update.effective_user

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_task FROM dialog_db
        WHERE id_task = ? AND id_user_tg = ?
        """,
        (task_id, user.id)
    )
    task_exists = cursor.fetchone()

    if task_exists:
        cursor.execute(
            """
            UPDATE dialog_db 
            SET description_task = ?
            WHERE id_user_tg = ? and id_task = ?
            """,
            (task_description, user.id, task_id)
        )
        conn.commit()
        await update.message.reply_text("Готово, я все обновила")
    else:
        await update.message.reply_text(
            "❓Задачи с таким id в базе данных нет. Попробуй ввести id задачи, которое существует."
            "\n\n💡Воспользуйся командой /list, чтобы увидеть все свои задачи, а потом снова выбери команду /update")
    conn.close()
    return ConversationHandler.END




async def del_task_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаление задачи по id задачи"""
    task_text = update.message.text
    user = update.effective_user
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    """Удаляется заявка по номеру задачи с проверкой совпадения id пользователя"""
    cursor.execute(
        """
        SELECT id_task FROM dialog_db
        WHERE id_task = ? AND id_user_tg = ?
        """,
        (task_text, user.id)
    )
    task_exists = cursor.fetchone()  # Проверяем, существует ли задача с таким id_task для данного пользователя

    if task_exists:
        cursor.execute(
            """
            DELETE FROM dialog_db
            WHERE id_task = ? AND id_user_tg = ?
            """,
            (task_text, user.id)
        )
        conn.commit()
        await update.message.reply_text("Готово, я все удалила")
    else:
        await update.message.reply_text("❓Задачи с таким id в базе данных нет. Попробуй ввести id задачи, которое существует."
        "\n\n💡Воспользуйся командой /list, чтобы увидеть все свои задачи, а потом снова выбери команду /update")
    conn.close()
    return ConversationHandler.END






async def list_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем все задачи из БД по пользователю. Далее отправляем задачи пользователю"""
    user = update.effective_user

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Получаем все задачи для данного пользователя
    cursor.execute(
        """
        SELECT id_task, description_task FROM dialog_db WHERE id_user_tg = ?
        """, (user.id,)
    )

    # Получаем результат запроса
    tasks = cursor.fetchall()

    conn.close()

    """Если задачи есть, мы возвращаем пользователю письмо со всеми его задачами
        В противном случае отправляем, что задач пока нет"""
    if tasks:
        tasks_text = "\n--------------------------------------------------\n".join(
            [f"id задачи: {task[0]}\nОписание задачи: {task[1]}" for task in tasks]
        )
        if update.message:
            await update.message.reply_text(tasks_text)
        # Иначе, проверяем, что это callback_query
        elif update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(tasks_text)


    else:
        if update.message:
            await update.message.reply_text("У тебя пока нет задач.")
        # Иначе, проверяем, что это callback_query
        elif update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text("У тебя пока нет задач.")
    return ConversationHandler.END

