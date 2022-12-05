from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from settings import TOKEN, ORDERS_CHAT_ID

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue


def main_keyboard(update: Update, context: CallbackContext):
    """Основаня клавиатура"""
    user = update.message.from_user

    job_queue.run_repeating(notify_assignees, interval=10.0, first=0.0, last=20.0, context=update.effective_chat.id)

    button_column = [['🔥Видео', 'Оставить заявку', 'О руководителе'], ['Наши контакты', 'Опрос']]

    main_kb = ReplyKeyboardMarkup([button for button in button_column], resize_keyboard=True)
    text = f'{user.first_name} {user.last_name} добрый день!!! Это Пожарский Роман руководитель отдела Alfa Digital Agency'

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='Скачать $10 млн.', callback_data='buy')]])
    message = context.bot.send_message(chat_id=update.effective_chat.id, text='Сделать навигацию',
                                       reply_markup=keyboard)
    context.bot.pin_chat_message(chat_id=message.chat_id, message_id=message.message_id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=main_kb)


def notify_assignees(context: CallbackContext):
    """ Спамим по таймеру"""
    context.bot.send_message(chat_id=context.job.context, text="Спам")


def show_video(update: Update, context: CallbackContext):
    """ Видео с ютуба """
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'https://www.youtube.com/watch?v=1fPWr0d5zBE')


def about_leader(update: Update, context: CallbackContext):
    """ О руководителе """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='О руководителе')


def about_us(update: Update, context: CallbackContext):
    """ О нас """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='О нас')


def order(update: Update, context: CallbackContext):
    """ Оставить заявку """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Что бы оставить завку напишите ваш номер телефона и имя в чат')


def poll(update: Update, context: CallbackContext):
    """ Опрос """
    user = update.message.from_user.username

    options_list = ['Вариант 1', 'Вариант 2', 'Вариант 3']

    message = context.bot.send_poll(chat_id=update.effective_chat.id,
                                    question=f'Опрос {update.message.text} создан пользователем {user}',
                                    options=options_list,
                                    is_anonymous=False,
                                    allows_multiple_answers=True)

    poll = {
        message.poll.id: {
            "admin_username": user,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
        }
    }
    context.bot_data.update(poll)


def inline_keys(update: Update, context: CallbackContext):
    """ Персылаем сообщение и выдаем сообщение с кнопками"""
    context.bot.forward_message(chat_id=ORDERS_CHAT_ID,
                                from_chat_id=update.message.chat_id,
                                message_id=update.message.message_id)

    buttons_data = {'Подписки на канал/страницу': 'subscriptions', 'Сообщение в лс телеграма': 'message',
                    'Заявки на сайте': 'order', 'Другое': 'other'}
    buttons = []
    for text, callback in buttons_data.items():
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback)])

    keyboard = InlineKeyboardMarkup([button for button in buttons])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Какие действия ожидаешь от рассылки?',
                             reply_markup=keyboard)


""" Старт """
dispatcher.add_handler(CommandHandler('start', main_keyboard))

""" Функции клавиатуры """
dispatcher.add_handler(MessageHandler(Filters.text('🔥Видео'), show_video))
dispatcher.add_handler(MessageHandler(Filters.text('Опрос'), poll))
dispatcher.add_handler(MessageHandler(Filters.text('Оставить заявку'), order))
dispatcher.add_handler(MessageHandler(Filters.text('О руководителе'), about_leader))
dispatcher.add_handler(MessageHandler(Filters.text('Наши контакты'), about_us))

""" Принимаем телефон и имя """
dispatcher.add_handler(
    MessageHandler(Filters.regex('^\+?(\+7|8|375)[-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}\s[A-ЯЁ][а-яё]+$'), inline_keys))

if __name__ == '__main__':
    updater.start_polling()
