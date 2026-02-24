from django.contrib import admin
from .models import Task




class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'category', 'status', 'deadline')
    list_filter = ('priority', 'status', 'category')
    search_fields = ('title', 'user__username')
    ordering = ('-created_at',)
    


admin.site.register(Task, TaskAdmin)