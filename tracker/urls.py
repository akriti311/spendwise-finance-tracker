from django.urls import path
from .views import home, delete_transaction

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
]