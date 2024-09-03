from django.conf.urls import url
from taskselection import views

urlpatterns = [
  url(r'^available_tasks/$', views.AvailableTaskList.as_view()),
  url(r'^selected_tasks/$', views.SelectedTaskList.as_view()),
  url(r'^select_task/(?P<code>[0-9]+)$', views.SelectTask.as_view())
]

