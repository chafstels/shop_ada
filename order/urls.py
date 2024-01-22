from django.urls import path
from .views import OrderAPIVIew, OrderConfirmView

urlpatterns = [
    path('', OrderAPIVIew.as_view()),
    path('confirm/<int:pk>/', OrderConfirmView.as_view()),
]
