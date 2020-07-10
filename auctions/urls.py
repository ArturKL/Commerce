from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlistng", views.new_listing, name="new_listing"),
    path("listings/<int:listing_id>", views.listing_view, name="listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid"),
    path("listings/<int:listing_id>/close", views.close, name='close')
]
