# challenges/urls.py
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet

router = DefaultRouter()
router.register('challenges', ChallengeViewSet, basename='challenge')
urlpatterns = router.urls
