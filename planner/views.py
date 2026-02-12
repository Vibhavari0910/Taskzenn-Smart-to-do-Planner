from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'