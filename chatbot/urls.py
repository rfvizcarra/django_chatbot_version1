from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot, name="chatbot"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("connect-gmail/", views.connect_gmail, name="connect_gmail"),
    path("gmail/callback/", views.gmail_callback, name="gmail_callback"),
]
