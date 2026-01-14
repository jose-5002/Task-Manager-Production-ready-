from django.urls import path
from .import views2

app_name = 'tasks'
urlpatterns = [
    path("", views2.view, name='view'),
    path("add/", views2.add, name='add'),
    path('tasks/', views2.CreateListTask.as_view(), name='CreateList'),
    path("tasks/<int:pk>/", views2.RetrieveUpdateDestroyTask.as_view(), name='RUD')
]