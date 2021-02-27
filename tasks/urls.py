from django.urls import path, re_path
from tasks.views import api_root_view, task_view, user_view 
from django.conf.urls import url

urlpatterns = [
    path('task', task_view.TaskList.as_view(), name='task-list'),
    # accept match any regEx after 'task/'
    re_path(r'^task\/(?P<pk>.+)$', task_view.TaskDetail.as_view()),
    path('user', user_view.UserList.as_view(), name='user-list'),
    path('user/signup', user_view.UserSignUp.as_view(), name='user-signup'),
    path('user/login', user_view.UserLogin.as_view(), name='user-login'),
    path('user/me', user_view.UserMeDetail.as_view(), name='user-me'),
    path('user/me/avatar', user_view.UserUploadDeleteAvatar.as_view(), name='user-me-avatar'),
]