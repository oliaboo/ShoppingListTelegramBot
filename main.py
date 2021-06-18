import telebot

API_TOKEN = "1751213583:AAE4zt3Ql-cF9eTQKWlEfKrv9PLuymyuH9Y"
shopping_bot = telebot.TeleBot(API_TOKEN)


commands = ["Add to list", "Get from list", "Remove from list"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)


# {<chat_id>: [shopping_list, current_operation, last_message_id]}
user_data = {}


@shopping_bot.message_handler(commands=["start"])
def start(message):
    shopping_bot.reply_to(message, "Welcome to shopping bot", reply_markup=keyboard)


@shopping_bot.message_handler(content_types=["text"])
def command(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = [[], None, None]
    if message.text == "Add to list":
        user_data[message.chat.id][1] = "add"
        shopping_bot.reply_to(message, "Now you can add items to the list")
    elif message.text == "Get from list":
        user_data[message.chat.id][1] = "get"
        shopping_bot.reply_to(message, ", ".join(user_data[message.chat.id][0]) if user_data[message.chat.id][0] else "No more items")
    elif message.text == "Remove from list":
        user_data[message.chat.id][1] = "rm"
        inline_kb = telebot.types.InlineKeyboardMarkup()
        inline_kb.row_width = 2
        for elem in user_data[message.chat.id][0]:
            inline_kb.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
        res = shopping_bot.reply_to(message, "Now you can delete items", reply_markup=inline_kb)
        user_data[message.chat.id][2] = res.message_id
    else:
        if user_data[message.chat.id][1] == "add":
            user_data[message.chat.id][0].append(message.text)
            shopping_bot.reply_to(message, f"successfully added {message.text}")


@shopping_bot.callback_query_handler(func=lambda x: True)
def callback_handler(call):
    index_to_remove = None
    for i in range(len(user_data[call.message.chat.id][0])):
        if user_data[call.message.chat.id][0][i] == call.data:
            index_to_remove = i
            break

    if index_to_remove is not None:
        del user_data[call.message.chat.id][0][index_to_remove]

    inline_kb = telebot.types.InlineKeyboardMarkup()
    inline_kb.row_width = 2
    for elem in user_data[call.message.chat.id][0]:
        inline_kb.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    shopping_bot.edit_message_reply_markup(call.message.chat.id, user_data[call.message.chat.id][2], reply_markup=inline_kb)


shopping_bot.polling()
