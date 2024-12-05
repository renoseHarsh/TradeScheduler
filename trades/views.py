from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .form import ScheduledTradeForm
from .models import ScheduledTrade


# Create your views here.
@login_required(login_url="users:login")
def schedule(request):
    if request.method == "POST":
        form = ScheduledTradeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
    return redirect("dashboard:index")


@login_required(login_url="users:login")
def delete(request):
    if request.method == "POST":
        trade = ScheduledTrade.objects.get(id=request.POST.get("trade_id"))
        if trade.user == request.user:
            print(trade)
            trade.delete()
    return redirect("dashboard:index")
