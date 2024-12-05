from django.urls import path

from .views import delete, recieve_hook, schedule, schedule_hook

app_name = "trades"

urlpatterns = [
    path("schedule/", schedule, name="schedule"),
    path("delete/", delete, name="delete"),
    path("schedule_hook/", schedule_hook, name="schedule_hook"),
    path("recieve_hook/", recieve_hook, name="recieve_hook"),
]
