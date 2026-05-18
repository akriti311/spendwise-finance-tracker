from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    delete_transaction,
    home,
    signup,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
]
