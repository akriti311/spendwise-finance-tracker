from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm


def home(request):
    transactions = Transaction.objects.all().order_by('-date')

    total_income = sum(
        t.amount for t in transactions if t.transaction_type == 'Income'
    )
    total_expense = sum(
        t.amount for t in transactions if t.transaction_type == 'Expense'
    )
    balance = total_income - total_expense

    # Category-wise expense summary
    expense_transactions = [t for t in transactions if t.transaction_type == 'Expense']
    category_summary = {}

    for transaction in expense_transactions:
        if transaction.category in category_summary:
            category_summary[transaction.category] += transaction.amount
        else:
            category_summary[transaction.category] = transaction.amount

    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'transactions': transactions,
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_summary': category_summary,
    }

    return render(request, 'tracker/home.html', context)


def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction.delete()
    return redirect('home')