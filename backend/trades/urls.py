from django.urls import path

from .views import delete_scheduled, get_scheduled, schedule, update_scheduled

app_name = "trades"

urlpatterns = [
    path("schedule/", schedule, name="schedule"),
    path("get_scheduled/", get_scheduled, name="get_scheduled"),
    path("update_scheduled/", update_scheduled, name="update_trade"),
    path("delete_scheduled/<str:pk>/", delete_scheduled, name="delete_scheduled"),
]
