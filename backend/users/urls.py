from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("user/", views.get_user, name="get_user"),
    path("tokens/", views.get_tokens, name="get_tokens"),
    path("updatetokens/", views.update_tokens, name="update_tokens"),
    path("accounts/", views.get_accounts, name="get_customers"),
]
