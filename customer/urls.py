from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="customer"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("search", views.search, name="search"),
    path("view", views.view, name="view"),
    path("reccomendation", views.reccomendation, name="reccomendation"),
    path("reserve", views.reserve, name="reserve"),
    path("positive", views.positive, name="positive"),
    path("negative", views.negative, name="negative"),
    path("alerts", views.alerts, name="alerts"),
]
