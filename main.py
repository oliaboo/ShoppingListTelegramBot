import telebot

API_TOKEN = "1751213583:AAE4zt3Ql-cF9eTQKWlEfKrv9PLuymyuH9Y"
shopping_bot = telebot.TeleBot(API_TOKEN)

# telebot.types.ReplyKeyboardMarkup
# telebot.types.InlineKeyboardMarkup

commands = ["Add to list", "Get from list", "Remove from list"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)

shopping_list = []
current_operation = None
last_message_id = None


@shopping_bot.message_handler(commands=["start"])
def start(message):
    shopping_bot.reply_to(message, "Welcome to shopping bot", reply_markup=keyboard)


@shopping_bot.message_handler(content_types=["text"])
def command(message):
    global current_operation
    global shopping_list
    global last_message_id
    if message.text == "Add to list":
        current_operation = "add"
        shopping_bot.reply_to(message, "Now you can add items to the list")
    elif message.text == "Get from list":
        current_operation = "get"
        shopping_bot.reply_to(message, ", ".join(shopping_list) if shopping_list else "No more items")
    elif message.text == "Remove from list":
        current_operation = "rm"
        inline_kb = telebot.types.InlineKeyboardMarkup()
        for elem in shopping_list:
            inline_kb.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
        res = shopping_bot.reply_to(message, "Now you can delete items", reply_markup=inline_kb)
        last_message_id = res.message_id
    else:
        if current_operation == "add":
            shopping_list.append(message.text)
            shopping_bot.reply_to(message, f"successfully added {message.text}")


@shopping_bot.callback_query_handler(func=lambda x: True)
def callback_handler(call):
    global shopping_list
    index_to_remove = None
    for i in range(len(shopping_list)):
        if shopping_list[i] == call.data:
            index_to_remove = i
            break

    if index_to_remove is not None:
        del shopping_list[index_to_remove]

    inline_kb = telebot.types.InlineKeyboardMarkup()
    for elem in shopping_list:
        inline_kb.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    shopping_bot.edit_message_reply_markup(call.message.chat.id, last_message_id, reply_markup=inline_kb)


shopping_bot.polling()
