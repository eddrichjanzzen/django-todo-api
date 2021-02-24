from django.urls import path
from tasks.views import api_root_view, task_view, user_view 

urlpatterns = [
    path('task', task_view.TaskList.as_view(), name='task-list'),
    path('task/<uuid:pk>/', task_view.TaskDetail.as_view()),
    path('user', user_view.UserList.as_view(), name='user-list'),
    path('user/signup', user_view.UserSignUp.as_view(), name='user-signup'),
    path('user/login', user_view.UserLogin.as_view(), name='user-login'),
    path('user/me', user_view.UserGetDetails.as_view()),
]