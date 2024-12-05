from django.urls import path

from .views import delete, execute, schedule

app_name = "trades"

urlpatterns = [
    path("schedule/", schedule, name="schedule"),
    path("delete/", delete, name="delete"),
    path("execute/", execute, name="execute"),
]
