import telebot
import random

# Заготовка для первого предложения
first = ["Сегодня — идеальный день для новых начинаний.",
         "Оптимальный день для того, чтобы решиться на смелый поступок!",
         "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
         "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
         "Плодотворный день для того, чтобы разобраться с накопившимися делами."]
second = ["Но помните, что даже в этом случае нужно не забывать про", "Если поедете за город, заранее подумайте про",
          "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
          "Если у вас упадок сил, обратите внимание на",
          "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
second_add = ["отношения с друзьями и близкими.",
              "работу и деловые вопросы, которые могут так некстати помешать планам.",
              "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
              "бытовые вопросы — особенно те, которые вы не доделали вчера.",
              "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
         "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
         "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
         "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
         "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]

TOKEN = ""  # Замените на  токен API

bot = telebot.TeleBot(TOKEN)
user_data = {} #словарь для хранения данных пользователей


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напишите /horoscope, чтобы получить гороскоп.")


@bot.message_handler(commands=['horoscope'])
def horoscope_command(message):
    zodiac_signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    keyboard = telebot.types.InlineKeyboardMarkup()

    for i, sign in enumerate(zodiac_signs):
        callback_data = f"zodiac:{i + 1}"
        button = telebot.types.InlineKeyboardButton(text=sign, callback_data=callback_data)
        keyboard.add(button)

    bot.reply_to(message, "Выберите ваш знак зодиака:", reply_markup=keyboard)
    user_data[message.chat.id] = zodiac_signs


@bot.callback_query_handler(func=lambda call: call.data.startswith('zodiac:'))
def process_zodiac_choice(call):
    _, zodiac_num = call.data.split(':')
    try:
        zodiac_num = int(zodiac_num)
        if 1 <= zodiac_num <= 12:
            zodiac_signs = user_data[call.message.chat.id]
            horoscope_data = (random.choice(first), random.choice(second), random.choice(second_add), random.choice(third))
            horoscope_text = "\n".join(horoscope_data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Ваш гороскоп ({zodiac_signs[zodiac_num - 1]}):\n{horoscope_text}", reply_markup=None)
            del user_data[call.message.chat.id] #удаляем после использования
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Неверный номер знака. Попробуйте ещё раз.", reply_markup=None)
    except (ValueError, KeyError):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ошибка обработки запроса.", reply_markup=None)


bot.infinity_polling()
