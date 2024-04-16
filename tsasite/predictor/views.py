from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

from .utils import get_records
from .models import Airport


def agent(request):
    return HttpResponse(b"Hello, World!")

def auth(request):
    return HttpResponse(b"Hello, World!")

def user(request):
    return HttpResponse(b"Hello, World!")

def results(request):
    ap = Airport.objects.get(pk="LAX")
    dt = datetime(year=2024, month=4, day=15, hour=11, minute=0, second=0)
    records = get_records(dt, ap, "CHK1", 1)

    template = loader.get_template("predictor/results.html")
    context = {"result": records[dt.strftime("%I %p").lower()]['y'],
               "times": list(records.keys()),
               "avgs": list(records.values())}
    return render(request, "predictor/results.html", context)
