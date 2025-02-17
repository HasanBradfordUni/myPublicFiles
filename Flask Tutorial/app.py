from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []
logins = []
timerStarted = False

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/set_timer', methods=['POST'])
def set_timer():
    task_name = request.form['task']
    task_duration = int(request.form['duration']) * 60  # Convert to seconds
    task_id = len(tasks) + 1  # Simple way to generate a task ID
    tasks.append({'id': task_id, 'task': task_name, 'duration': task_duration, 'time_remaining': task_duration})
    return redirect(url_for('index'))

@app.route('/update_timer', methods=['POST'])
def update_timer():
    data = request.get_json()
    task_id = int(data['taskId'])
    time_remaining = int(data['timeRemaining'])
    for task in tasks:
        if task['id'] == task_id:
            task['time_remaining'] = time_remaining
            break
    return jsonify({'status': 'success'})

@app.route('/registerPage')
def registerPage():
    return render_template('register.html')

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        return 'Passwords do not match'
    logins.append({'username': username, 'password': password})
    return redirect(url_for('loginPage'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    for login in logins:
        if login['username'] == username and login['password'] == password:
            return redirect(url_for('index'))
    return 'Invalid login'

@app.route('/getTasks', methods=['GET'])
def getTasks():
    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run(host='localhost', port=5050)