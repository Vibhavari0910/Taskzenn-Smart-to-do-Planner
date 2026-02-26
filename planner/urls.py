from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import CustomLogoutView

urlpatterns = [

    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('register/', views.register, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', views.update_task, name='update_task'),
    path('tasks/complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),

    path('profile/', views.profile, name='profile'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('tasks/today/', views.todays_task, name='todays_task'),

    path('about/', views.about, name='about'),
]