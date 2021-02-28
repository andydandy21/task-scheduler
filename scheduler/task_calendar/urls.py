from django.urls import path

from . import views

urlpatterns = [
    path('', views.MonthlyCalendarView.as_view(), name='month-view'),
    path('task/new/', views.TaskCreateView.as_view(), name='create-task'),
    path('daily/', views.DailyTaskList.as_view(), name='daily-list'),
    path('dates/', views.DateSelectorView.as_view(), name='date-selector'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
]
