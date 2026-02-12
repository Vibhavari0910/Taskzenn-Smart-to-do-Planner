from django.urls import path
from .views import home,register
from .views import CustomLoginView
from .views import CustomLogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

