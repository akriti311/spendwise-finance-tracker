from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TransactionForm
from .models import Transaction


def signup(request):
    """Create a new account and log the user in automatically."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to SpendWise! Your account was created.')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'tracker/signup.html', {'form': form})


class UserLoginView(LoginView):
    """Log in with username and password (Django's built-in view)."""
    template_name = 'tracker/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You are now logged in.')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Log out securely (POST-only, Django best practice)."""
    pass


@login_required
def home(request):
    """Dashboard: only this user's transactions."""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_income = sum(
        t.amount for t in transactions if t.transaction_type == 'Income'
    )
    total_expense = sum(
        t.amount for t in transactions if t.transaction_type == 'Expense'
    )
    balance = total_income - total_expense

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
            form.save(user=request.user)
            messages.success(request, 'Transaction added successfully.')
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


@login_required
def delete_transaction(request, transaction_id):
    """Delete only if the transaction belongs to the logged-in user."""
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )
    transaction.delete()
    messages.success(request, 'Transaction deleted.')
    return redirect('home')
