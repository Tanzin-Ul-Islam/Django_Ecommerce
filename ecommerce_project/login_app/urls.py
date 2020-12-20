from django.urls import path
from login_app import views

app_name = "login_app"

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_sys, name='login'),
    path('logout/', views.logout_sys, name='logout'),
    path('profile/', views.user_profile, name='profile'),
]