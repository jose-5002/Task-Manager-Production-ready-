from django.urls import path
from rest_framework.routers import DefaultRouter
from .import views2, views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'tasks'
router = DefaultRouter()
router.register("tasks", views.TaskViewSet, basename='task')

urlpatterns = [
    path("", views2.view, name='view'),
    path("add/", views2.add, name='add'),
    path('tasks/', views2.CreateListTask.as_view(), name='CreateList'),
    path("tasks/<int:pk>/", views2.RetrieveUpdateDestroyTask.as_view(), name='RUD'),

    path("login/", views.login_view.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    router.urls,
]
