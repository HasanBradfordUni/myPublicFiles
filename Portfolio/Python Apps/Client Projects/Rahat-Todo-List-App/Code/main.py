from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import sqlite3
import uuid

app = Flask(__name__)  # Create a Flask app

# Database setup
DB_PATH = 'todo_app.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tasks table with device_id
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT NOT NULL,
        content TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()

init_db()

def get_device_id():
    # Check if device_id exists in cookies
    device_id = request.cookies.get('device_id')
    
    # If no device_id, create a new one
    if not device_id:
        device_id = str(uuid.uuid4())
    
    return device_id

@app.route('/')  # Define a route
def home():
    device_id = get_device_id()
    
    # Connect to database and get tasks for this device
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, content, completed FROM tasks WHERE device_id = ?', (device_id,))
    tasks = [dict(row) for row in c.fetchall()]
    conn.close()
    
    # Create response with tasks and set cookie if needed
    response = make_response(render_template('index.html', tasks=tasks))
    
    # Set the device_id cookie if it doesn't exist
    if not request.cookies.get('device_id'):
        # Set cookie to expire in 10 years (plenty of time)
        response.set_cookie('device_id', device_id, max_age=60*60*24*365*10)
    
    return response

@app.route('/add_task', methods=['POST'])
def add_task():
    device_id = get_device_id()
    task_content = request.form['task_content']
    
    if task_content.strip():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO tasks (device_id, content, completed) VALUES (?, ?, ?)', 
                 (device_id, task_content, False))
        conn.commit()
        conn.close()
        
    response = make_response(redirect(url_for('home')))
    
    # Set cookie if it doesn't exist
    if not request.cookies.get('device_id'):
        response.set_cookie('device_id', device_id, max_age=60*60*24*365*10)
        
    return response

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    device_id = get_device_id()
    new_content = request.form['new_content']
    
    if new_content.strip():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE tasks SET content = ? WHERE id = ? AND device_id = ?', 
                 (new_content, task_id, device_id))
        conn.commit()
        conn.close()
        
    return redirect(url_for('home'))

@app.route('/remove_task/<int:task_id>')
def remove_task(task_id):
    device_id = get_device_id()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ? AND device_id = ?', (task_id, device_id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('home'))

@app.route('/remove_multiple_tasks', methods=['POST'])
def remove_multiple_tasks():
    device_id = get_device_id()
    task_ids = request.form.getlist('task_ids')
    
    if task_ids:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Use parameterized query for safety
        placeholders = ','.join(['?'] * len(task_ids))
        query = f'DELETE FROM tasks WHERE id IN ({placeholders}) AND device_id = ?'
        
        # Add device_id as the last parameter
        params = task_ids + [device_id]
        
        c.execute(query, params)
        conn.commit()
        conn.close()
    
    return redirect(url_for('home'))

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    device_id = get_device_id()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # First get the current state
    c.execute('SELECT completed FROM tasks WHERE id = ? AND device_id = ?', (task_id, device_id))
    task = c.fetchone()
    
    if task:
        new_state = not bool(task[0])
        c.execute('UPDATE tasks SET completed = ? WHERE id = ? AND device_id = ?', 
                 (new_state, task_id, device_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('localhost')