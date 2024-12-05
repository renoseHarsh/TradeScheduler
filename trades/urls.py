from django.urls import path

from .views import delete, schedule

app_name = "trades"

urlpatterns = [
    path("schedule/", schedule, name="schedule"),
    path("delete/", delete, name="delete"),
]
