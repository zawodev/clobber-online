# users/urls.py
from django.urls import path
from .views import (
    RegisterView, ConfirmEmailView, LoginView,
    ProfileView, FriendAddView, SendFriendRequestView, CurrentUserView,
    RespondFriendRequestView, IncomingFriendRequestsView, AvatarUploadView, ObtainTokenFromSessionView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('confirm/<uuid:token>/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<str:username>/', ProfileView.as_view()),
    path('friend-request/send/', SendFriendRequestView.as_view()),
    path('friend-request/incoming/', IncomingFriendRequestsView.as_view()),
    path('friend-request/<int:pk>/respond/', RespondFriendRequestView.as_view()),
    path('avatar/upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('token/', ObtainTokenFromSessionView.as_view(), name='token-from-session'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
