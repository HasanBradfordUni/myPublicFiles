import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from financeOptions import FinanceOptions
from accounts import Accounts
from account import Account

class FinanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Fulcrum - GUI")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize backend components
        self.accounts = Accounts()
        self.finance_options = FinanceOptions()
        self.current_user = None
        
        # Create main interface
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Finance Fulcrum", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel for buttons
        button_frame = ttk.LabelFrame(main_frame, text="Finance Options", padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Finance operation buttons
        buttons = [
            ("Add Income", self.add_income),
            ("Add Expense", self.add_expense),
            ("View Balance", self.view_balance),
            ("View Total Income", self.view_total_income),
            ("View Total Expenses", self.view_total_expenses),
            ("View Finance History", self.view_finance_history),
            ("Generate Report", self.generate_report),
            ("Clear Output", self.clear_output)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=20)
            btn.grid(row=i, column=0, pady=5, sticky=tk.W)
        
        # Right panel for input and output
        input_output_frame = ttk.Frame(main_frame)
        input_output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_output_frame.columnconfigure(0, weight=1)
        input_output_frame.rowconfigure(1, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(input_output_frame, text="Input Area", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Amount input
        ttk.Label(input_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=15)
        self.amount_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Date input
        ttk.Label(input_frame, text="Date (dd/mm/yyyy):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        self.date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Note input
        ttk.Label(input_frame, text="Note (optional):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.note_var = tk.StringVar()
        self.note_entry = ttk.Entry(input_frame, textvariable=self.note_var, width=15)
        self.note_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Report date inputs
        report_frame = ttk.LabelFrame(input_frame, text="Report Date Range", padding="5")
        report_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        report_frame.columnconfigure(1, weight=1)
        report_frame.columnconfigure(3, weight=1)
        
        ttk.Label(report_frame, text="Start:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.start_date_var = tk.StringVar(value="01/01/2025")
        self.start_date_entry = ttk.Entry(report_frame, textvariable=self.start_date_var, width=12)
        self.start_date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(report_frame, text="End:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.end_date_entry = ttk.Entry(report_frame, textvariable=self.end_date_var, width=12)
        self.end_date_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Output area
        output_frame = ttk.LabelFrame(input_output_frame, text="Output", padding="10")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=50, height=20, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initial welcome message
        self.append_output("Welcome to Finance Fulcrum GUI!\n")
        self.append_output("Use the buttons on the left to perform finance operations.\n")
        self.append_output("Enter amounts, dates, and notes in the input area above.\n\n")
    
    def append_output(self, text):
        """Append text to the output area"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """Clear the output area"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Output cleared")
    
    def validate_amount(self):
        """Validate and return the amount input"""
        try:
            amount = float(self.amount_var.get())
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount (number)")
            return None
    
    def validate_date(self, date_str):
        """Validate date format"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in dd/mm/yyyy format")
            return False
    
    def add_income(self):
        """Add income transaction"""
        amount = self.validate_amount()
        if amount is None:
            return
        
        date = self.date_var.get()
        if not self.validate_date(date):
            return
        
        # Add to finance options
        self.finance_options.ReportGenerator.setDate(date)
        self.finance_options.IncomeInput(amount)
        
        # Handle note if provided
        note = self.note_var.get().strip()
        if note:
            income_id = self.finance_options.ReportGenerator.getID(
                self.finance_options.FinanceHistory.used_positions - 1
            )
            self.finance_options.NotesManager.notes.append((income_id, note))
        
        # Update output
        self.append_output(f"✓ Income added: ${amount:.2f} on {date}\n")
        if note:
            self.append_output(f"  Note: {note}\n")
        self.append_output("\n")
        
        # Clear inputs
        self.amount_var.set("")
        self.note_var.set("")
        self.status_var.set(f"Income of ${amount:.2f} added successfully")
    
    def add_expense(self):
        """Add expense transaction"""
        amount = self.validate_amount()
        if amount is None:
            return
        
        date = self.date_var.get()
        if not self.validate_date(date):
            return
        
        # Add to finance options
        self.finance_options.ReportGenerator.setDate(date)
        self.finance_options.ExpensesInput(amount)
        
        # Handle note if provided
        note = self.note_var.get().strip()
        if note:
            expense_id = self.finance_options.ReportGenerator.getID(
                self.finance_options.FinanceHistory.used_positions - 1
            )
            self.finance_options.NotesManager.notes.append((expense_id, note))
        
        # Update output
        self.append_output(f"✓ Expense added: ${amount:.2f} on {date}\n")
        if note:
            self.append_output(f"  Note: {note}\n")
        self.append_output("\n")
        
        # Clear inputs
        self.amount_var.set("")
        self.note_var.set("")
        self.status_var.set(f"Expense of ${amount:.2f} added successfully")
    
    def view_balance(self):
        """Display current balance"""
        balance = self.finance_options.TotalBalanceCalc()
        self.append_output(f"💰 Current Balance: ${balance:.2f}\n\n")
        self.status_var.set("Balance calculated")
    
    def view_total_income(self):
        """Display total income"""
        total_income = self.finance_options.IncomeOutput()
        self.append_output(f"📈 Total Income: ${total_income:.2f}\n\n")
        self.status_var.set("Total income displayed")
    
    def view_total_expenses(self):
        """Display total expenses"""
        total_expenses = self.finance_options.ExpensesOutput()
        self.append_output(f"📉 Total Expenses: ${total_expenses:.2f}\n\n")
        self.status_var.set("Total expenses displayed")
    
    def view_finance_history(self):
        """Display finance history"""
        self.append_output("📊 Finance History:\n")
        self.append_output("-" * 30 + "\n")
        
        finance_history = self.finance_options.FinanceHistory.show_all()
        if not finance_history:
            self.append_output("No transactions recorded yet.\n\n")
            return
        
        for i, amount in enumerate(finance_history):
            transaction_id = self.finance_options.ReportGenerator.getID(i)
            date = self.finance_options.ReportGenerator.getDate(transaction_id)
            transaction_type = "Income" if amount > 0 else "Expense"
            
            self.append_output(f"{i+1}. {transaction_type}: ${abs(amount):.2f} on {date}\n")
            self.append_output(f"   ID: {transaction_id}\n")
            
            # Check for notes
            if self.finance_options.NotesManager.hasNotes(transaction_id):
                for note_id, note_text in self.finance_options.NotesManager.notes:
                    if note_id == transaction_id:
                        self.append_output(f"   Note: {note_text}\n")
            self.append_output("\n")
        
        self.status_var.set("Finance history displayed")
    
    def generate_report(self):
        """Generate finance report for date range"""
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        if not self.validate_date(start_date) or not self.validate_date(end_date):
            return
        
        try:
            finance_history = self.finance_options.FinanceHistory.show_all()
            total_income, total_expenses, dated_transactions = self.finance_options.ReportGenerator.generateReport(
                start_date, end_date, finance_history
            )
            
            self.append_output("📋 FINANCE REPORT\n")
            self.append_output("=" * 40 + "\n")
            self.append_output(f"Period: {start_date} to {end_date}\n")
            self.append_output(f"Total Income: ${total_income:.2f}\n")
            self.append_output(f"Total Expenses: ${total_expenses:.2f}\n")
            self.append_output(f"Net Amount: ${total_income - total_expenses:.2f}\n")
            self.append_output("-" * 40 + "\n")
            
            if dated_transactions:
                self.append_output("Transactions in this period:\n")
                for transaction in dated_transactions:
                    transaction_type = "Income" if transaction.amount > 0 else "Expense"
                    self.append_output(f"• {transaction.date}: {transaction_type} ${abs(transaction.amount):.2f}\n")
                    if transaction.notes:
                        self.append_output(f"  Note: {transaction.notes}\n")
            else:
                self.append_output("No transactions found in this period.\n")
            
            self.append_output("\n")
            self.status_var.set("Report generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")

def main():
    root = tk.Tk()
    app = FinanceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()