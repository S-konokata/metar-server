from django.contrib.auth.views import logout_then_login
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
