from django.urls import path, include
from taskselection import views

urlpatterns = [
  path('available_tasks/', views.AvailableTaskList.as_view()),
  path('selected_tasks/', views.SelectedTaskList.as_view()),
  path('select_task/<code>', views.SelectTask.as_view()),
]

