from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('api/v1/login/', login),
    # path('api/v1/logout/', logout),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/signup/', signup),
    path('api/v1/profile/', profile),
    path('api/v1/forgot-password/', forgot_password),
    path('api/v1/reset-password/', reset_password),
]

