from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="business"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("edit", views.edit, name="edit"),
    path("analytics", views.analytics, name="analytics"),
    path("spots", views.spots, name="spots"),
    path("positive", views.positive, name="positive"),
    path("negative", views.negative, name="negative"),
    path("alerts", views.alerts, name="alerts"),
]

app_name = "business"
