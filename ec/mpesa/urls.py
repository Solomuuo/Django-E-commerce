from django.urls import path
from mpesa.views import mpesa_callback, stk_push_view, transaction_history

urlpatterns = [
    path("stk-push/", stk_push_view, name="stk_push"),
    path('transactions/', transaction_history, name='transaction_history'),
    path("stk_callback/", mpesa_callback, name="mpesa_callback"),
]
