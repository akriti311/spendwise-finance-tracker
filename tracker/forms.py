from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True, user=None):
        """Attach the logged-in user so every transaction is user-specific."""
        instance = super().save(commit=False)
        if user is not None:
            instance.user = user
        if commit:
            instance.save()
        return instance