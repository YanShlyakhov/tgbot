from flask import Flask, url_for, request, abort
import time
import dataset

db = dataset.connect('sqlite:///qqq')

users = db['users']
history = db['history']
tasks = db['tasks']

app = Flask(__name__)

task_str = "https://dribbble.com/shots/7150930-Social-Landing-page"

names_ready = {}

names_for_work = []

users_online = {}

online = 0

def get_names():
    global names_for_work
    names_for_work = []
    f = open("logins.txt", "r")
    for login in f.readlines():
        names_for_work.append(login[:-1])

@app.route('/task_add', methods=['POST'])
def handle_data():
    global task_str
    task_str = request.form['task']
    get_names()
    return ""

@app.route('/')
def api_root():
    return """
<form action="/task_add" method="post">
    <input type="text" name="task">
    <input type="submit">
</form>
            """

@app.route("/add", methods=["POST"])
def add():
    name = request.json.get('name')
    nick = request.json.get('nick')

    global users
    user = users.find_one(name=name)

    if users == None:
        users.insert(dict(name = name, nick = nick, likes = 0))
        return "", 201
    
    return "", 501

@app.route("/like", methods=['GET'])
def likes():
    name = request.json.get('name')
    url  = request.json.get('url')

    global users
    global tasks
    user = users.find_one(name = name)
    if user == None:
        return "", 501
    
    if user['likes'] >= 2:
        user['likes']-=2
        users.update(user, ['id'])
        tasks.insert(dict(url = url))
        return "", 201
    else:
        return "", 501

@app.route('/task', methods = ['GET'])
def tasksGive():
    global users
    global history
    nick = request.json.get('nick')
    user = users.find_one(dict(nick = nick))

    if user == None:
        return "", 501

    for t in tasks:
        url = t['url']
        h = history.find_one(dict(url = url, nick = nick))
        if h == None:
            user['likes'] += 1
            users.update(user, ['id'])
            history.insert(dict(url = url, nick = nick))
            return url
    return "", 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)