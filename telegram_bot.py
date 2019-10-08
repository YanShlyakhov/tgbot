import telebot

bot = telebot.TeleBot('679851125:AAHtjabEfaWIV5oKKJj-LAc_W5ESawLUd0I')

def get_nick(s):
    return s[s.find("add ") + 4:]

def get_url(s):
    return s[s.find("like ") + 5:]

def get_likes(name):
    return 2

@bot.message_handler(content_types=['text'])
def send_text(message):
    name = message.from_user.username #id
    if "add" in message.text:
        nick_name = get_nick(message.text)
        bot.send_message(message.chat.id, name + 'added user with nick: ' + nick_name)
    elif "like" in message.text:
        free_likes = get_likes(name)
        if free_likes >= 2:
            url = get_url(message.text)
            bot.send_message(message.chat.id, name + 'added url to likes: ' + url)
        else:
            bot.send_message(message.chat.id, name + " you dont have a likes to continue this operation")
    
    print(name)
    
bot.polling()
