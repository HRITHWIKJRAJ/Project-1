from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('login',views.login,name="login"),
    path('logout',views.logout, name="logout"),
    path('home',views.home, name="home"),
    path('<id>/',views.details,name="details"),
    path('review',views.chat,name="chat"),
]