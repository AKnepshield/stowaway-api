from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from stowawayapi import views
from stowawayapi.views import (
    register_user,
    login_user,
    get_current_user,
    RecordView,
    ConditionView,
)
from stowawayapi.views.genre_view import GenreView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"records", RecordView, "record")
router.register(r"conditions", ConditionView, "condition")
router.register(r"genres", GenreView, "genre")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("current_user", get_current_user),
    path("records/liked/", RecordView.as_view({"get": "liked"}), name="liked-records"),
]
