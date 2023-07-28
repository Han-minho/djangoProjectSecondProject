from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login'),
]