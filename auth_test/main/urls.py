from django.urls import path
from . import views

app_name = "main"   

urlpatterns = [
    path('' , views.home_page_request , name='home_page'),
    path('register' , views.register_request , name='register'),
    path('register_error', views.register_error , name='register_error'),
    path('login' , views.login_request , name='login'),
    path('logout' , views.logout_request , name= 'logout'),
]
