from django.urls import path

from .views import LoginView, RegisterView, index, LogoutView

app_name = 'login'
urlpatterns = [
    path('', index, name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]