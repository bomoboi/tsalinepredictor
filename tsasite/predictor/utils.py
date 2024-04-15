from .models import Record, Airport
from django.db.models import Avg, Max, Q
from datetime import datetime, timedelta

"""
To get the histogram of how this time compares to other times:
We need the data for the time we're at
We also need the data for the surrounding times
    which should be variable b/c it would b nice to
    reuse in the agent view
So we need to get the records for the day we're on
for all three years + the records for surrounding times

"""

def get_records(date: datetime,
                airport: Airport,
                checkpoint: str,
                var_hour: int):

    start_time = date - timedelta(hours=var_hour)
    end_time = date + timedelta(hours=var_hour)

    qs = Record.objects.filter(
        ap=airport
    ).filter(
        checkpoint=checkpoint)

    avg_set = {}
    for h in range(-var_hour, var_hour+1):
        filter_date = date + timedelta(hours=h)
        h_qs = qs.filter(
            date__hour=filter_date.hour
        ).filter(
            date__day=filter_date.day
        ).filter(
            date__year__lt=filter_date.year
        )
        avg_set[str(h)] = h_qs.aggregate(Avg("pax", default=0))["pax__avg"]
    return avg_set
