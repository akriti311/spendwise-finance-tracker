from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'date', 'user')
    list_filter = ('transaction_type', 'category', 'user')
    search_fields = ('title', 'user__username')
