from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .utils import get_records
from .models import Airport
from .forms import AuthForm, UserForm

@login_required
def agent(request):
    return HttpResponse(b"Hello, World!")

def auth(request):

    if request.method == "POST":
        form = AuthForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect("/simulator/")

    else:
        form = AuthForm()

    return render(request, "predictor/auth.html", {"form": form})

def user(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            dt = form.cleaned_data["date"]
            chk = form.cleaned_data["checkpoint"]
            ap = form.cleaned_data["ap"]
            records = get_records(dt,ap,chk, 1)
            print(records)

            context  = {"result": records[dt.strftime("%I %p").lower()]['y'],
               "times": list(records.keys()),
               "avgs": list(records.values())}

            return render(request, "predictor/results.html", context)
    else:
        form = UserForm()
    return render(request, "predictor/user.html", {"form": form})

def results(request):

    ap = Airport.objects.get(pk="LAX")
    dt = datetime(year=2024, month=4, day=15, hour=11, minute=0, second=0)
    records = get_records(dt, ap, "CHK1", 1)

    context = {"result": records[dt.strftime("%I %p").lower()]['y'],
               "times": list(records.keys()),
               "avgs": list(records.values())}

    return HttpResponse(f"")
    #return render(request, "predictor/results.html", context)
