from django.urls import path
from rest_framework.routers import DefaultRouter
from .import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'tasks'
router = DefaultRouter()
router.register("tasks", views.TaskViewSet, basename='task')
router.register("profile", views.ProfileViewSet, basename='profile')

urlpatterns = [

    path("login/", views.login_view.as_view(), name='login'),
    path("register/", views.register_user, name='register'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
