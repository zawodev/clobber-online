# users/urls.py
from django.urls import path
from .views import (
    RegisterView, ConfirmEmailView, LoginView,
    ProfileView, FriendAddView, SendFriendRequestView,
    RespondFriendRequestView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('confirm/<uuid:token>/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<str:username>/', ProfileView.as_view()),
    path('friend-request/send/', SendFriendRequestView.as_view()),
    path('friend-request/<int:pk>/respond/', RespondFriendRequestView.as_view()),
]
