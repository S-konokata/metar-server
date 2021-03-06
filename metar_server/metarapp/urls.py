from django.urls import path
from . import views

app_name = 'metarapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
