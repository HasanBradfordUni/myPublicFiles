from flask import Flask, render_template, request, redirect, url_for, flash
from accounts import Accounts
import getpass

app = Flask(__name__)
app.secret_key = 'your_secret_key'

accounts = Accounts()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add login logic here
        flash('Login functionality not implemented yet.')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if password == confirm_password:
            accounts.add_account(email, password)
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match.')
    return render_template('register.html')

@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = getpass.getpass(prompt="Enter the old password (digits only): ")
        new_password = getpass.getpass(prompt="Enter the new password (digits only): ")
        if accounts.update_password(username, old_password, new_password):
            flash("Password updated successfully.")
        else:
            flash("Incorrect username or password.")
    return render_template('update_password.html')

@app.route('/save_accounts', methods=['POST'])
def save_accounts():
    filename = request.form['filename']
    accounts.save_accounts(filename)
    if accounts.get_account_count() > 0:
        flash("Accounts downloaded successfully!")
    else:
        flash("No accounts to download!")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='localhost', port=6922)