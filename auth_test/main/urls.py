from django.urls import path
from . import views

app_name = "main"   

urlpatterns = [
    path('' , views.home_page_request , name='home_page'),
    path('register' , views.register_request , name='register'),
    path('login' , views.login_request , name='login'),
    path('register_error', views.register_error , name='register_error'),
    path('login_error' , views.login_error , name='login_error'),
    path('error_auth' , views.error_auth , name='error_auth'),
    path('logout' , views.logout_request , name='logout'),
    path('test' , views.test_html , name='test'),
]
