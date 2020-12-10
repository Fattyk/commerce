from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("createList", views.createList, name="createList"),
    path("<int:id>", views.listing, name="listing"),
    path("add_remove_watch/<int:id>", views.add_remove_watch, name="add_remove_watch"),
    path("remove_listing/<int:id>", views.remove_listing, name="remove_listing"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watch", views.watch, name="watch"),
    path("won", views.won, name="won")
]
