from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
import os
from models.accounts import Accounts
from models.account import Account
from models.finance_options import FinanceOptions

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Initialize global instances
accounts = Accounts()
user_finance_options = {}  # Store finance options per user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        account = accounts.get_account(username)
        if account and account.Login(username, password):
            session['username'] = username
            session['logged_in'] = True
            
            # Initialize finance options for this user
            if username not in user_finance_options:
                user_finance_options[username] = FinanceOptions()
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if accounts.get_account(username):
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        account = Account(username, password, "basic")
        accounts.add_account(account)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        account = accounts.get_account(session['username'])
        if account:
            account.logout()
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    username = session['username']
    finance_opts = user_finance_options.get(username)
    
    if finance_opts:
        balance = finance_opts.TotalBalanceCalc()
        total_income = finance_opts.IncomeOutput()
        total_expenses = finance_opts.ExpensesOutput()
    else:
        balance = total_income = total_expenses = 0
    
    return render_template('dashboard.html', 
                         username=username,
                         balance=balance,
                         total_income=total_income,
                         total_expenses=total_expenses)

@app.route('/finance')
def finance():
    if not session.get('logged_in'):
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    return render_template('finance.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    username = session['username']
    finance_opts = user_finance_options.get(username)
    
    if not finance_opts:
        return jsonify({'success': False, 'message': 'Finance options not initialized'})
    
    try:
        transaction_type = request.form['type']
        amount = float(request.form['amount'])
        date = request.form['date']
        note = request.form.get('note', '').strip()
        
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')
        
        # Convert date to dd/mm/yyyy format for backend
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d/%m/%Y')
        
        # Add transaction
        finance_opts.ReportGenerator.setDate(formatted_date)
        
        if transaction_type == 'income':
            finance_opts.IncomeInput(amount)
        else:
            finance_opts.ExpensesInput(amount)
        
        # Add note if provided
        if note:
            transaction_id = finance_opts.ReportGenerator.getID(
                finance_opts.FinanceHistory.used_positions - 1
            )
            finance_opts.NotesManager.notes.append((transaction_id, note))
        
        return jsonify({
            'success': True, 
            'message': f'{transaction_type.capitalize()} of ${amount:.2f} added successfully'
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid amount or date format'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_finance_data')
def get_finance_data():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    username = session['username']
    finance_opts = user_finance_options.get(username)
    
    if not finance_opts:
        return jsonify({'success': False, 'message': 'No finance data'})
    
    balance = finance_opts.TotalBalanceCalc()
    total_income = finance_opts.IncomeOutput()
    total_expenses = finance_opts.ExpensesOutput()
    
    # Get transaction history
    history = []
    finance_history = finance_opts.FinanceHistory.show_all()
    
    for i, amount in enumerate(finance_history):
        transaction_id = finance_opts.ReportGenerator.getID(i)
        date = finance_opts.ReportGenerator.getDate(transaction_id)
        transaction_type = "Income" if amount > 0 else "Expense"
        
        # Get note if exists
        note = ""
        for note_id, note_text in finance_opts.NotesManager.notes:
            if note_id == transaction_id:
                note = note_text
                break
        
        history.append({
            'id': transaction_id,
            'type': transaction_type,
            'amount': abs(amount),
            'date': date,
            'note': note
        })
    
    return jsonify({
        'success': True,
        'balance': balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'history': history
    })

@app.route('/generate_report', methods=['POST'])
def generate_report():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    username = session['username']
    finance_opts = user_finance_options.get(username)
    
    if not finance_opts:
        return jsonify({'success': False, 'message': 'No finance data'})
    
    try:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Convert dates to dd/mm/yyyy format
        start_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        start_formatted = start_obj.strftime('%d/%m/%Y')
        end_formatted = end_obj.strftime('%d/%m/%Y')
        
        finance_history = finance_opts.FinanceHistory.show_all()
        total_income, total_expenses, dated_transactions = finance_opts.ReportGenerator.generateReport(
            start_formatted, end_formatted, finance_history
        )
        
        transactions = []
        for transaction in dated_transactions:
            transactions.append({
                'date': transaction.date,
                'amount': transaction.amount,
                'type': 'Income' if transaction.amount > 0 else 'Expense',
                'notes': transaction.notes
            })
        
        return jsonify({
            'success': True,
            'start_date': start_formatted,
            'end_date': end_formatted,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_amount': total_income - total_expenses,
            'transactions': transactions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)