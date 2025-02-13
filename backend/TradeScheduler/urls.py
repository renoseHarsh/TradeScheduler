from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/trades/", include("trades.urls")),
    re_path(r"^(?!admin|api).*",TemplateView.as_view(template_name='dist/index.html')),
]
