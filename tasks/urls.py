from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.task_list),
    path('tasks/<uuid:pk>/', views.task_detail),
]