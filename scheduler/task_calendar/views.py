from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from calendar import monthrange

from .forms import TaskForm
from .models import Task


class MonthlyCalendarView(ListView):
    model = Task
    template_name = 'task_calendar/monthly_calendar.html'
    context_object_name = 'task_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        context['current_date'] = d
        context['date_list'] = calendar_list(d.year, d.month)
        context['next_month'] = next_month(d)
        context['prev_month'] = prev_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.now()

def next_month(d):
    days_in_month = monthrange(d.year, d.month)
    last_day = d.replace(day=days_in_month[1])
    month = last_day + timedelta(days=1)
    month = 'month=' + month.strftime("%Y-%m")
    return month

def prev_month(d):
    first_day = d.replace(day=1)
    month = first_day - timedelta(days=1)
    month = 'month=' + month.strftime("%Y-%m")
    return month

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_calendar/new_task.html'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_calendar/task_detail.html'

class DailyTaskList(ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'task_calendar/daily_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_date = get_day(self.request.GET.get('day', None))
        context['myday'] = list_date
        context['task_list'] = Task.objects.filter(start_time__date = list_date)
        context['next_day'] = next_day(list_date)
        context['prev_day'] = prev_day(list_date)
        return context

def get_day(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.now()

def next_day(list_date):
    next_list_date = list_date + timedelta(days=1)
    next_list_date = 'day=' + next_list_date.strftime('%Y-%m-%d')
    return next_list_date

def prev_day(list_date):
    prev_list_date = list_date - timedelta(days=1)
    prev_list_date = 'day=' + prev_list_date.strftime('%Y-%m-%d')
    return prev_list_date

class DateSelectorView(ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'task_calendar/date_selector.html'
    ordering = 'start_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from_date = get_day(self.request.GET.get('from', None))
        to_date = get_day(self.request.GET.get('to', None))
        date_range = date_list(from_date, to_date)
        context['date_list'] = date_range
        return context


def date_list(from_date, to_date):
    moving_date = from_date
    date_list = []
    
    while moving_date != to_date + timedelta(days=1):
        date_list.append(moving_date)
        moving_date = moving_date + timedelta(days=1)
    
    return date_list




def calendar_list(year, month):
    
    first_day = date(year, month, 1)
    days_in_month = monthrange(year, month) 
    last_day = date(year, month, days_in_month[1])
    prev_month_overflow = int(first_day.strftime("%w"))
    next_month_overflow = 6 - int(last_day.strftime("%w"))
    cal_start_date = first_day - timedelta(days=prev_month_overflow)
    cal_end_date = last_day + timedelta(days=next_month_overflow)
    
    mylist = []
    
    moving_date = cal_start_date
    while moving_date != cal_end_date + timedelta(days=1):
        mylist.append(moving_date)
        moving_date = moving_date + timedelta(days=1)

    return mylist