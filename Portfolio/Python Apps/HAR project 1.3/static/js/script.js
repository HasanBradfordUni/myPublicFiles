// Handle transaction form submission
document.getElementById('transactionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/add_transaction', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Clear form
            this.reset();
            document.getElementById('date').valueAsDate = new Date();
            
            // Show success message
            showAlert(data.message, 'success');
            
            // Reload finance data
            loadFinanceData();
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('An error occurred while adding the transaction.', 'danger');
    });
});

// Handle report form submission
document.getElementById('reportForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/generate_report', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayReport(data);
        } else {
            showAlert(data.message, 'danger');
        }
    })
    .catch(error => {
        showAlert('An error occurred while generating the report.', 'danger');
    });
});

// Load finance data
function loadFinanceData() {
    fetch('/get_finance_data')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update overview
            document.getElementById('balance').textContent = `$${data.balance.toFixed(2)}`;
            document.getElementById('totalIncome').textContent = `$${data.total_income.toFixed(2)}`;
            document.getElementById('totalExpenses').textContent = `$${data.total_expenses.toFixed(2)}`;
            
            // Update history
            displayTransactionHistory(data.history);
        }
    })
    .catch(error => {
        console.error('Error loading finance data:', error);
    });
}

// Display transaction history
function displayTransactionHistory(history) {
    const historyList = document.getElementById('historyList');
    
    if (history.length === 0) {
        historyList.innerHTML = '<p class="text-muted">No transactions recorded yet.</p>';
        return;
    }
    
    let html = '';
    history.forEach(transaction => {
        const typeClass = transaction.type.toLowerCase();
        html += `
            <div class="transaction-item ${typeClass}">
                <div class="d-flex justify-content-between">
                    <div>
                        <strong>${transaction.type}: $${transaction.amount.toFixed(2)}</strong>
                        <br>
                        <small class="text-muted">${transaction.date} • ID: ${transaction.id}</small>
                        ${transaction.note ? `<br><small><em>${transaction.note}</em></small>` : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    historyList.innerHTML = html;
}

// Display report
function displayReport(reportData) {
    const reportOutput = document.getElementById('reportOutput');
    const reportContent = document.getElementById('reportContent');
    
    let html = `
        <div class="alert alert-info">
            <h6>Report for ${reportData.start_date} to ${reportData.end_date}</h6>
            <p><strong>Total Income:</strong> $${reportData.total_income.toFixed(2)}</p>
            <p><strong>Total Expenses:</strong> $${reportData.total_expenses.toFixed(2)}</p>
            <p><strong>Net Amount:</strong> $${reportData.net_amount.toFixed(2)}</p>
        </div>
    `;
    
    if (reportData.transactions.length > 0) {
        html += '<h6>Transactions in this period:</h6>';
        reportData.transactions.forEach(transaction => {
            html += `
                <div class="transaction-item ${transaction.type.toLowerCase()}">
                    <strong>${transaction.type}: $${Math.abs(transaction.amount).toFixed(2)}</strong>
                    <br>
                    <small class="text-muted">${transaction.date}</small>
                    ${transaction.notes ? `<br><small><em>${transaction.notes}</em></small>` : ''}
                </div>
            `;
        });
    } else {
        html += '<p class="text-muted">No transactions found in this period.</p>';
    }
    
    reportContent.innerHTML = html;
    reportOutput.style.display = 'block';
}

// Show alert messages
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}