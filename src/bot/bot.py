from telebot import TeleBot, types
import requests
import json
TOKEN = "7399074434:AAH-DGrBjf4fSel4OQyZ7L7jLu3LxwJb3tE"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    bot.send_message(message.chat.id, "Пришлите фото паллета в чат и я скажу, есть ли на нём повреждения")

@bot.message_handler()
def handle_message(message: types.Message):
    bot.send_message(message.chat.id, "Не понимаю, о чём вы")

def create_keyboard():
    kb = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(
        text="Да",
        callback_data='yes'
    )
    no_button = types.InlineKeyboardButton(
        text="Нет",
        callback_data='no'
    )
    kb.row(yes_button, no_button)
    return kb

def handle_user_answer(query: types.CallbackQuery):
    bot.answer_callback_query(
        callback_query_id=query.id
    )
    bot.send_message(
        chat_id=query.message.chat.id,
        text=f'Принято, спасибо!'
    )


@bot.callback_query_handler(
    func=handle_user_answer
)


@bot.message_handler(content_types=["photo"])
def handle_photo(message: types.Message):
    url = 'http://palette-app:8000/infer/'
    file_path = bot.get_file(message.photo[-1].file_id).file_path
    file = bot.download_file(file_path)
    with open("temp.png", "wb") as code:
        code.write(file)
    files = {'file': file}
    r = requests.post(url, files=files)
    result = 'Без дефекта' if json.loads(r.text)['class_name'] == 'OK' else "Сломанный"
    bot.send_message(
        chat_id=message.chat.id,
        text=result,
        reply_markup=create_keyboard()
    )

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)