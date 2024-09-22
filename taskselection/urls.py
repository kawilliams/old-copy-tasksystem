# taskselection/urls.py
# from django.urls import path
# from taskselection import views

# urlpatterns = [
#   path('available_tasks/', views.AvailableTaskList.as_view()),
#   path('selected_tasks/', views.SelectedTaskList.as_view()),
#   path('select_task/<code>', views.SelectTask.as_view()),
# ]

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
#from .views import AvailableTaskList, SelectedTaskList, SelectTask
from taskselection import views

urlpatterns = format_suffix_patterns([
    path("", views.api_root),
    path('tasks/', 
        views.AvailableTaskList.as_view(),
        name='task-list'),
    path('tasks/<int:pk>/', 
        views.SelectTask.as_view(),
        name='task-detail'),
    path('tasks/<int:pk>/highlight/', 
        views.TaskHighlight.as_view(),
        name='task-highlight'),
    # path("<str:room_name>/", views.room, name="room"),
    path('users/', 
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/', 
        views.UserDetail.as_view(),
        name='user-detail')    
])
# path('available_tasks/', AvailableTaskList.as_view(), name='available-tasks'),
# path('selected_tasks/', SelectedTaskList.as_view(), name='selected-tasks'),
# path('select_task/<int:code>', SelectTask.as_view(), name='select-task'),

