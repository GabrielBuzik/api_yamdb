from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, signup, send_token

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name="signup"),
    path('v1/auth/token/', send_token, name='send_token'),
]
