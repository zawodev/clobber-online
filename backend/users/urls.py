# users/urls.py
from django.urls import path
from .views import (
    RegisterView, ActivateView, ProfileView, ProfileDetailView,
    FriendRequestListView, SendFriendRequestView,
    FriendRequestAcceptView, FriendRequestRejectView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='user-activate'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('profile/<username>/', ProfileDetailView.as_view(), name='user-profile-detail'),
    path('friends/requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('friends/send/<username>/', SendFriendRequestView.as_view(), name='friend-request-send'),
    path('friends/accept/<int:pk>/', FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friends/reject/<int:pk>/', FriendRequestRejectView.as_view(), name='friend-request-reject'),
]
