from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("relabel/<int:pk>/", views.relabel, name="relabel"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("retrain/", views.retrain, name="retrain"),
]
