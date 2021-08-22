from django.urls import path

from .views import HomeView, AddView, EventView, home

app_name = 'map'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('add/', AddView.as_view(), name='add'),
    path('event/<int:id>/', EventView.as_view(), name='event'),
    path('map/', home),
]