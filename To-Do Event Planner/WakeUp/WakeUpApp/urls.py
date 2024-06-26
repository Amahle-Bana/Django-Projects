from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("completedTasks", views.completedTasks, name="completedTasks"),
    path("notifications", views.notifications, name="notifications"),
    path("favourites", views.favourites, name="favourites"),
    path("settings", views.settings, name="settings"),
]