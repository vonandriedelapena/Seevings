from django.shortcuts import render

def transaction_list(request):
    # Displays all transactions
    return render(request, 'transactionList.html')

def create_transaction(request):
    # Lets user choose transaction type (Transfer, Expense, Income, Saving)
    # Redirects to the appropriate "Add Transaction" page
    return render(request, 'createTransaction.html')

def add_transfer(request):
    return render(request, 'addTransfer.html')

def transfer_list(request):
    return render(request, 'transferList.html')

def add_expense(request):
    return render(request, 'addExpense.html')

def expense_list(request):
    return render(request, 'expenseList.html')

def add_income(request):
    return render(request, 'addIncome.html')

def income_list(request):
    return render(request, 'incomeList.html')

def add_saving(request):
    return render(request, 'addSaving.html')

def saving_list(request):
    return render(request, 'savingList.html')
