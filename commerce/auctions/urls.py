from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("close_bid", views.close_bid, name="close_bid"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("my_bid", views.my_bid, name="my_bid"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:title>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist")
]
