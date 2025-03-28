# Bot_tasks
## Описание

Этот Telegram-бот предназначен для управления задачами. Он позволяет пользователям добавлять, обновлять, удалять и просматривать свои задачи с помощью команд и кнопок в меню.

## Функциональность

Добавление задач

Обновление задач

Удаление задач

Просмотр списка всех задач

## Установка

### Библиотеки:

python-telegram-bot

Собственные модули .env

### Конфигурация

Создайте файл .env и укажите в нем токен бота, а также администратор

#### Пример:
BOT_TOKEN= 1705052328922:AAE-vgHAfOeDDtgA5sjGwJUoXRdjTGxSK_7o

ADMIN_IDS= 1705052328922

## Использование

### Запуск бота:

python main.py

### Команды бота:

/start – запустить бота и открыть меню управления задачами.

/add – добавить новую задачу.

/update – обновить существующую задачу.

/del – удалить задачу.

/list – показать все задачи.

### Структура кода

start() – обработчик команды /start, который отправляет пользователю меню кнопок.

add_task_button() и add_task_command() – обработчики добавления задач.

update_task_button(), update_task_command(), get_task_id_for_update() – обработчики обновления задач.

del_task_button() и del_task_command() – обработчики удаления задач.

list_task_button() и list_task_command() – обработчики вывода списка задач.

handle_text() – обработчик текстовых сообщений вне команд.

### Разработка

Этот бот использует ConversationHandler для работы с диалогами и InlineKeyboardMarkup для создания кнопок.

