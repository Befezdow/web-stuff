import telebot
from telebot import types
import config
from database import Mongo

mongo_instance = Mongo(uri=config.mongo_uri)
mongo_instance.db.drop_collection('users')

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['hello'])
def say_hello(message):
    bot.send_message(message.chat.id, 'Hello, master')


@bot.message_handler(commands=['mongo'])
def get_mongo(message):
    bot.send_message(message.chat.id, 'count is {}'.format(mongo_instance.db['users'].count()))


@bot.message_handler(commands=['new'])
def add_user(message):
    res = mongo_instance.db['users'].find_one({'user_id': message.user_from.id})
    if res.count() > 0:
        bot.send_message(message.chat.id, 'You already registered, email: {}'.format(res['email']))
        return
    msg = bot.send_message(message.chat.id, 'Creating new user... \nEnter email:password')
    bot.register_next_step_handler(msg, register_user)


def register_user(message):
    if message.text == '/refuse':
        bot.send_message(message.chat.id, 'Create canceled.')
    elif ':' not in message.text:
        msg = bot.send_message(message.chat.id, 'Incorrect string. Missed ":"')
        bot.register_next_step_handler(msg, register_user)
    else:
        credentials = message.text.split(':')
        mongo_instance.db['users'].insert_one({
            'email': credentials[0],
            'password': credentials[1],
            'user_id': message.user_from.id
        })
        bot.send_message(message.chat.id, 'Successful registration.')


@bot.message_handler(commands=['mail'])
def check_email(message):
    # checking email
    current_user = mongo_instance.db['users'].find_one({'user_id': message.user_from.id})
    if current_user.count == 0:
        bot.send_message(message.chat.id, 'Unknown user, you need to register first, type /new for register')
        return
    else:
        bot.send_message(message.chat.id, 'Your email is {}'.format(current_user['email']))
    markup = types.ReplyKeyboardMarkup()
    markup.row('All unread messages')
    markup.row('Last five messages')
    markup.row('All messages')
    msg = bot.send_message(message.chat.id, 'What mode of fetch you prefer?', reply_markup=markup)
    bot.register_next_step_handler(msg, get_emails)


def get_emails(message):
    answer = message.text
    delete_markup = types.ReplyKeyboardRemove()
    if answer == 'All unread messages':
        bot.send_message(message.chat.id, 'Want all unread messages', reply_markup=delete_markup)
    elif answer == 'Last five messages':
        bot.send_message(message.chat.id, 'Want five messages', reply_markup=delete_markup)
    elif answer == 'All messages':
        bot.send_message(message.chat.id, 'Want ALL messages', reply_markup=delete_markup)
    else:
        msg = bot.send_message(message.chat.id, 'Wrong option. Try again')
        bot.register_next_step_handler(msg, get_emails)
        return


@bot.message_handler(func=lambda message: 'пидор' in message.text.lower())
def fuck_off(message):
    bot.send_message(message.chat.id, 'Сам ты пидор, пидор.')


@bot.message_handler()
def default_handler(message):
    bot.send_message(message.chat.id, "I don't give a fuck")


if __name__ == '__main__':
    bot.polling(none_stop=True)
