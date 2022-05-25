
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:writerid>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("compose", views.compose, name="compose"),
    path("load_posts/<str:posttype>", views.load_posts, name="load_posts"),
    path("load_profile_posts/<int:id>", views.load_profile_posts, name="load_profile_posts")
]
