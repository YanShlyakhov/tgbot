import telebot
import requests

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
        r = requests.post("http://127.0.0.1:5000/add", json={'name':name, 'nick':nick_name})
        bot.send_message(message.chat.id, name + 'added user with nick: ' + nick_name)
    elif "like" in message.text:
        url = get_url(message.text)
        r = requests.get("http://127.0.0.1:5000/add", json= {'name' : name, 'url':url})
        if r.status_code == 201:
            bot.send_message(message.chat.id, name + 'added url to likes: ' + url)
        else:
            bot.send_message(message.chat.id, name + " you dont have a likes to continue this operation")
    
    print(name)
    
bot.polling()
