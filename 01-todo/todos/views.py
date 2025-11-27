from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task


def task_list(request):
    from datetime import date, datetime
    
    all_tasks = Task.objects.all()
    today = timezone.now().date()
    
    # Categorize tasks
    overdue_tasks = []
    today_tasks = []
    upcoming_tasks = []
    no_due_date_tasks = []
    
    for task in all_tasks:
        if not task.is_resolved:
            if task.due_date:
                task_date = task.due_date.date() if hasattr(task.due_date, 'date') else task.due_date
                if task_date < today:
                    overdue_tasks.append(task)
                elif task_date == today:
                    today_tasks.append(task)
                else:
                    upcoming_tasks.append(task)
            else:
                no_due_date_tasks.append(task)
    
    # Get completed tasks
    completed_tasks = all_tasks.filter(is_resolved=True)
    
    context = {
        'overdue_tasks': overdue_tasks,
        'today_tasks': today_tasks,
        'upcoming_tasks': upcoming_tasks,
        'no_due_date_tasks': no_due_date_tasks,
        'completed_tasks': completed_tasks,
        'total_tasks': all_tasks.count(),
        'active_tasks': all_tasks.filter(is_resolved=False).count(),
    }
    
    return render(request, 'todos/home.html', context)


def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')
        reminder_date = request.POST.get('reminder_date')
        
        task = Task(title=title, description=description)
        if due_date:
            task.due_date = due_date
        if reminder_date:
            task.reminder_date = reminder_date
        task.save()
        return redirect('task_list')
    
    return render(request, 'todos/task_form.html', {'action': 'Create'})


def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')
        reminder_date = request.POST.get('reminder_date')
        
        if due_date:
            task.due_date = due_date
        else:
            task.due_date = None
            
        if reminder_date:
            task.reminder_date = reminder_date
        else:
            task.reminder_date = None
            
        task.save()
        return redirect('task_list')
    
    return render(request, 'todos/task_form.html', {'task': task, 'action': 'Edit'})


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todos/task_confirm_delete.html', {'task': task})


def task_toggle_resolve(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_resolved = not task.is_resolved
    task.save()
    return redirect('task_list')


def calendar_view(request):
    import calendar
    from datetime import date
    
    # Get current month and year, or from request parameters
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Get all tasks for the month
    all_tasks = Task.objects.filter(
        due_date__year=year,
        due_date__month=month
    )
    
    # Create calendar
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Organize tasks by day
    tasks_by_day = {}
    for task in all_tasks:
        day = task.due_date.day
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)
    
    # Convert keys to strings for template compatibility
    tasks_by_day_str = {str(k): v for k, v in tasks_by_day.items()}
    
    # Calculate next/previous month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    context = {
        'calendar': cal,
        'month_name': month_name,
        'year': year,
        'month': month,
        'tasks_by_day': tasks_by_day,
        'tasks_by_day_str': tasks_by_day_str,
        'next_month': next_month,
        'next_year': next_year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'today': today.date(),
    }
    
    return render(request, 'todos/calendar.html', context)

