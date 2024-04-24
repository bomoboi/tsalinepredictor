from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime

from .utils import get_records
from .models import Airport, Record
from .forms import AuthForm, UserForm, SimForm

def home(request):
    return render(request, "predictor/home.html")

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

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
            ap = Airport.objects.get(pk=form.cleaned_data["ap"])
            records = get_records(dt, ap, var_hour=2)

            context  = {"result": records[dt.strftime("%I %p").lower()]['y'],
               "times": list(records.keys()),
               "avgs": list(records.values())}

            return render(request, "predictor/results.html", context)
    else:
        form = UserForm()
    return render(request, "predictor/user.html", {"form": form})

@login_required(login_url="/predictor/auth/")
def agent(request):
    if request.method == "POST":
        print("POST")
        form = SimForm(request.POST)

        if form.is_valid():
            dt = form.cleaned_data["date"]
            ap = Airport.objects.get(pk=form.cleaned_data["ap"])
            num_agents = form.cleaned_data["num_agents"]
            records = get_records(dt, ap, var_hour=2)

            context  = {"result": records[dt.strftime("%I %p").lower()]['y'],
                "times": list(records.keys()),
                        "avgs": list(records.values()),
                        "agents": num_agents,
                        "ap": form.cleaned_data["ap"]}

            return render(request, "predictor/sim.html", context)
    else:
        print("NOT POST")
        form = SimForm()
    return render(request, "predictor/agent.html", {"form": form})


"""
def results(request):

    ap = Airport.objects.get(pk="LAX")
    dt = datetime(year=2024, month=4, day=15, hour=11, minute=0, second=0)
    records = get_records(dt, ap, "CHK1", 1)

    context = {"result": records[dt.strftime("%I %p").lower()]['y'],
               "times": list(records.keys()),
               "avgs": list(records.values())}

    return HttpResponse(f"Results page")
    #return render(request, "predictor/results.html", context)
"""
