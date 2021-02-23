from django.urls import path
from tasks.views import api_root_view, task_view, user_view 

urlpatterns = [
    path('tasks/', task_view.TaskList.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/', task_view.TaskDetail.as_view()),
    path('users/', user_view.UserList.as_view(), name='user-list'),
    path('users/<uuid:pk>/', user_view.UserDetail.as_view()),
]