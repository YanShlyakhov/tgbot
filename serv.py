from flask import Flask, url_for, request
app = Flask(__name__)

task_str = "https://dribbble.com/shots/7150930-Social-Landing-page"

@app.route('/task_add', methods=['POST'])
def handle_data():
    global task_str
    task_str = request.form['task']
    return ""

@app.route('/')
def api_root():
    return """
<form action="/task_add" method="post">
    <input type="text" name="task">
    <input type="submit">
</form>
            """

@app.route('/task')
def api_articles():
    global task_str
    return task_str

if __name__ == '__main__':
    app.run()