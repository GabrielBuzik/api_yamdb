from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, signup, send_token

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name="signup"),
    path('auth/token/', send_token, name='send_token'),
]