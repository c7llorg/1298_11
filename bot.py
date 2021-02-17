import telebot
import re
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import service
import bot_token

bot = telebot.TeleBot(bot_token.token)
bot.delete_webhook()

help_message = '/warehouse - список основного склада\n\
        /remote - список удаленного склада'

@bot.message_handler(commands=['warehouse'])
def warehouse(message):
    warehouse = service.get_positions()
    for n, position in enumerate(warehouse):
        bot.send_message(message.chat.id,
        reply_markup=gen_markup(position, n + 1),
        text=f"{'-'.join(position.get('id'))} | {position.get('name')}")

def gen_markup(position, n):
    if position.get('name') == '-':
        return None
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Выдать', callback_data=str(n)))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None)
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id, text=re.sub(r'\| \w+\s*\S*', '| -', call.message.text))
    service.checkout(int(call.data))
    bot.answer_callback_query(call.id, "ok")

@bot.message_handler(commands=['remote'])
def warehouse(message):
    remote = '\n'.join([x.get('name') for x in service.get_remote()])
    if not remote:
        remote = 'Удаленный склад пуст'
    bot.send_message(message.chat.id, remote)

@bot.message_handler(content_types=['document'])
def upload(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, service.upload(downloaded_file))

@bot.message_handler(commands=['checkout'])
def checkout(message):
    checkout_list = service.get_checkout_list()
    bot.send_message(message.chat.id, '\n'.join([x.get('name') + ' из ' + '-'.join(x.get('id')) for x in checkout_list]))

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
