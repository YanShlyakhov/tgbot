from flask import Flask, url_for, request, abort
import time
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

def online_users():
    global users_online
    global online
    now = time.clock()
    for user in users_online:
        if now - user.value() < 180000:
            online -= 1

@app.route('/task/<username>')
def api_articles(username):
    global task_str
    global names_ready
    global online
    global users_online
    print(username)
    online_users()
    if username not in names_for_work:
        abort(404)

    if username not in names_ready.keys():
        names_ready[username] = []
        users_online[username] = time.clock()
        online += 1
        
    if task_str in names_ready[username]:
        abort(404)

    users_online[username] = time.clock()
    names_ready[username].append(task_str)
    return task_str

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)