# rooms/urls.py
from django.urls import path
from .views import rooms, join_room

urlpatterns = [
    path('rooms/',      rooms,     name='rooms'),       # GET list, POST create
    path('rooms/join/', join_room, name='join-room'),   # POST join
]
