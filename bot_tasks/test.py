import unittest
from unittest.mock import patch, MagicMock
from telegram import Update, Message, Chat, CallbackQuery
from telegram.ext import CallbackContext

from main import (
    start,
    add_task_button,
    add_task_command,
    update_task_button,
    update_task_command,
    del_task_button,
    del_task_command,
    list_task_button,
    list_task_command,
    handle_text,
    done,
)
#Тесты уточнены у ИИ
class TestBot(unittest.TestCase):

    def setUp(self):
        self.chat = MagicMock(spec=Chat)
        self.message = MagicMock(spec=Message)
        self.message.chat = self.chat
        self.update = MagicMock(spec=Update)
        self.context = MagicMock(spec=CallbackContext)

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_start(self, mock_update, mock_context):
        mock_update.message.reply_html = MagicMock()
        mock_update.effective_user.first_name = "TestUser"
        await start(mock_update, mock_context)
        mock_update.message.reply_html.assert_called_once()

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_add_task_button(self, mock_update, mock_context):
        mock_update.callback_query = MagicMock(spec=CallbackQuery)
        mock_update.callback_query.message.reply_text = MagicMock()
        await add_task_button(mock_update, mock_context)
        mock_update.callback_query.message.reply_text.assert_called_once_with(text="Введите задачу, которую хотите добавить")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_add_task_command(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await add_task_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(text="Введите задачу, которую хотите добавить")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_update_task_button(self, mock_update, mock_context):
        mock_update.callback_query = MagicMock(spec=CallbackQuery)
        mock_update.callback_query.message.reply_text = MagicMock()
        await update_task_button(mock_update, mock_context)
        mock_update.callback_query.message.reply_text.assert_called_once_with(text="Введите id задачи, которую вы хотите отредактировать")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_update_task_command(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await update_task_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(text="Введите id задачи, которую вы хотите отредактировать")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_del_task_button(self, mock_update, mock_context):
        mock_update.callback_query = MagicMock(spec=CallbackQuery)
        mock_update.callback_query.message.reply_text = MagicMock()
        await del_task_button(mock_update, mock_context)
        mock_update.callback_query.message.reply_text.assert_called_once_with(text="Введите номер задачи, которую вы хотите удалить")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_del_task_command(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await del_task_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(text="Введите номер задачи, которую вы хотите удалить")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_list_task_button(self, mock_update, mock_context):
        mock_update.callback_query = MagicMock(spec=CallbackQuery)
        mock_update.callback_query.message.reply_text = MagicMock()
        await list_task_button(mock_update, mock_context)
        mock_update.callback_query.message.reply_text.assert_called_once_with(text="Вот, что мне удалось получить:")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_list_task_command(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await list_task_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(text="Вот, что мне удалось получить:")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_handle_text(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await handle_text(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("К сожалению, я не знаю, что ответить. Если у тебя есть какой-либо запрос, попробуй воспользоваться командами через /start")

    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    async def test_done(self, mock_update, mock_context):
        mock_update.message.reply_text = MagicMock()
        await done(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("Готово")

if __name__ == "__main__":
    unittest.main()
