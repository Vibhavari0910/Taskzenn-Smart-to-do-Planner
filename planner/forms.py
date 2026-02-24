from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from django.utils.timezone import now

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Task
        exclude = ['user', 'status','created_at', 'updated_at']