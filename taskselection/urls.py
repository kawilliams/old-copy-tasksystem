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
    path('available_tasks/', 
        views.AvailableTaskList.as_view(),
        name='available-tasks'),
    path('selected_tasks/', 
        views.SelectedTaskList.as_view(),
        name='selected-tasks'),
    path('select_task/<int:code>/', 
        views.SelectTask.as_view(),
        name='task-detail'),
    path('tasks/<int:code>/highlight/', 
        views.TaskHighlight.as_view(),
        name='task-highlight'),
    path('users/', 
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/', 
        views.UserDetail.as_view(),
        name='user-detail'),  
    ## Test message passing by visiting http://127.0.0.1:8000/room/
    # path("<str:room_name>/", views.room, name="room")
    ### End message passing test 
])
# path('available_tasks/', AvailableTaskList.as_view(), name='available-tasks'),
# path('selected_tasks/', SelectedTaskList.as_view(), name='selected-tasks'),
# path('select_task/<int:code>', SelectTask.as_view(), name='select-task'),

