from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path("create_application", views.create_application),
    path("delete/<int:id>", views.delete_application),
    path("update/<int:id>", views.update_application),
    path("rebuild/<int:id>", views.rebuild_application),
    path("clone/<int:id>", views.clone_application),
]
