from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .utils import get_records
from .models import Airport
from .forms import AuthForm, UserForm

@login_required(login_url="/predictor/auth/")
def simulator(request):
    return HttpResponse(b"Hello, Simulator!")

def auth(request):
    form = AuthForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        agent = form.login(request)
        if agent is not None:
            login(request, agent)
            return redirect(request.POST.get('next'))

    return render(request, "predictor/auth.html", {"form": form})

def user(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            dt = form.cleaned_data["date"]
            chk = form.cleaned_data["checkpoint"]
            ap = form.cleaned_data["ap"]
            records = get_records(dt,ap,chk, 1)

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
