# taskselection/urls.py
# from django.urls import path
# from taskselection import views

# urlpatterns = [
#   path('available_tasks/', views.AvailableTaskList.as_view()),
#   path('selected_tasks/', views.SelectedTaskList.as_view()),
#   path('select_task/<code>', views.SelectTask.as_view()),
# ]

from django.urls import path, include
#from .views import AvailableTaskList, SelectedTaskList, SelectTask
from rest_framework.routers import DefaultRouter
from taskselection import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]


# path('available_tasks/', AvailableTaskList.as_view(), name='available-tasks'),
# path('selected_tasks/', SelectedTaskList.as_view(), name='selected-tasks'),
# path('select_task/<int:code>', SelectTask.as_view(), name='select-task'),

