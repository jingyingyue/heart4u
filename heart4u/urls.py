from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile_view, name="profile"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("follow", views.follow_user, name="follow"),
    path("unfollow", views.unfollow_user, name="unfollow"),
    path("search", views.search, name="search"),
    path("upload", views.upload_view, name="upload"),
    path("<str:username>/post/<int:post_id>", views.post_view, name="post"),
    path("like_unlike", views.like_unlike, name="like_unlike"),
    path("comment", views.comment, name="comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)