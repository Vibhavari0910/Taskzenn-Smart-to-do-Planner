from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib import messages
from datetime import date, timedelta
from .forms import RegisterForm, TaskForm


# Home
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



# Login / Logout
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = 'login'


# ✅ DASHBOARD (Main Logic)
@login_required
def dashboard(request):

    tasks = Task.objects.filter(
        user=request.user,
        is_deleted=False
    )
    search_query = request.GET.get('search')

    if search_query:
       tasks = tasks.filter(title__icontains=search_query)

    # 🔍 Filters
    category = request.GET.get('category')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    date_filter = request.GET.get('date')

    if category:
        tasks = tasks.filter(category=category)

    if status:
        if status == 'Overdue':
            tasks = [t for t in tasks if t.is_overdue]
        else:
            tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    # 🔥 Date Filters
    today = date.today()

    if date_filter == "today":
        tasks = tasks.filter(deadline=today)

    elif date_filter == "tomorrow":
        tasks = tasks.filter(deadline=today + timedelta(days=1))

    elif date_filter == "week":
        week_end = today + timedelta(days=7)
        tasks = tasks.filter(deadline__range=(today, week_end))

    elif date_filter == "overdue":
        tasks = [t for t in tasks if t.is_overdue]

    # Convert safely to list
    tasks_list = list(tasks)

    # 📊 Statistics
    total_tasks = len(tasks_list)
    completed_tasks = len([t for t in tasks_list if t.status == 'Completed'])
    pending_tasks = len([t for t in tasks_list if t.status == 'Pending'])
    overdue_tasks = len([t for t in tasks_list if t.is_overdue])

    productivity = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    

    # ===============================
    # 📅 WEEKLY PRODUCTIVITY
    # ===============================

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week - timedelta(days=1)

    this_week_tasks = Task.objects.filter(
        user=request.user,
        is_deleted=False,
        deadline__range=[start_of_week, end_of_week]
    )

    this_week_total = this_week_tasks.count()
    this_week_completed = this_week_tasks.filter(status='Completed').count()

    this_week_productivity = (
        int((this_week_completed / this_week_total) * 100)
        if this_week_total > 0 else 0
    )

    last_week_tasks = Task.objects.filter(
        user=request.user,
        is_deleted=False,
        deadline__range=[start_of_last_week, end_of_last_week]
    )

    last_week_total = last_week_tasks.count()
    last_week_completed = last_week_tasks.filter(status='Completed').count()

    last_week_productivity = (
        int((last_week_completed / last_week_total) * 100)
        if last_week_total > 0 else 0
    )

    trend = this_week_productivity - last_week_productivity

    # ===============================
    # 🔔 OVERDUE ALERT COUNT
    # ===============================

    overdue_count = Task.objects.filter(
    user=request.user,
    is_deleted=False,
    status='Pending',
   deadline=today
    ).count()

    # ===============================
    # FINAL CONTEXT
    # ===============================

    context = {
        'tasks': tasks_list,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'productivity': productivity,
        'this_week_productivity': this_week_productivity,
        'last_week_productivity': last_week_productivity,
        'trend': trend,
        'overdue_count': overdue_count,
        'this_week_productivity': this_week_productivity,
        'last_week_productivity': last_week_productivity,
        'trend': trend,
        'overdue_count': overdue_count,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user   # VERY IMPORTANT
            task.save()
            messages.success(request, "Task saved successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form})

# Complete Task
@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'Completed'
    task.save()
    messages.success(request, "Task marked as completed")
    return redirect('dashboard')


# Soft Delete
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_deleted = True
    task.save()
    messages.success(request, "Task deleted")
    return redirect('dashboard')

@login_required
def profile(request):
    tasks = Task.objects.filter(
        user=request.user,
        is_deleted=False
    )

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()

    productivity = (
        int((completed_tasks / total_tasks) * 100)
        if total_tasks > 0 else 0
    )

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'productivity': productivity,
    }

    return render(request, 'profile.html', context)

@login_required
def all_tasks(request):
    tasks = Task.objects.filter(
        user=request.user,
        is_deleted=False
    ).order_by('-created_at')

    return render(request, 'all_tasks.html', {'tasks': tasks})

@login_required
def todays_task(request):
    today = date.today()

    tasks = Task.objects.filter(
        user=request.user,
        deadline=today,
        is_deleted=False
    )

    return render(request, 'todays_task.html', {'tasks': tasks})

def about(request):
    return render(request, 'about.html')