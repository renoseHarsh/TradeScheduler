from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from TradeScheduler.decorators import anonymous_required

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import AccessToken


# Create your views here.
@anonymous_required
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
        return redirect("dashboard:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@anonymous_required
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("dashboard:index")
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required(login_url="/users/login/")
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    return redirect("dashboard:index")


@login_required(login_url="/users/login/")
def add_access_token(request):
    if request.method == "POST":
        accessToken = request.POST.get("accessToken")
        try:
            access_token = request.user.accesstoken
            access_token.token = accessToken
            access_token.save()
        except AccessToken.DoesNotExist:
            AccessToken.objects.create(user=request.user, token=accessToken)

    return redirect("dashboard:index")
