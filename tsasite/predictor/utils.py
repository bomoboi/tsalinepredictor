from .models import Record, Airport
from django.db.models import Avg
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

    # gets the initial QuerySet
    qs = Record.objects.filter(
        ap=airport
    ).filter(
        checkpoint=checkpoint)

    avg_dict = {}
    for h in range(-var_hour, var_hour+1):
        # gets the data for each hour across all years
        # in the database
        # HACK maybe change this to pre-covid only?
        # or an option for admin
        filter_date = date + timedelta(hours=h)
        h_qs = qs.filter(
            date__hour=filter_date.hour
        ).filter(
            date__day=filter_date.day
        ).filter(
            date__year__lt=filter_date.year
        )
        # creates a dictionary where the keys are in the format 10 am, 11am ,etc
        # and the values are the average time for that hour
        avg_dict[
            filter_date.strftime("%I %p").lower()] = h_qs.aggregate(
            Avg("pax", default=0))["pax__avg"]

        # make sure the central value is highlighted in a different color
    avg_dict[date.strftime("%I %p").lower()] = {"y": avg_dict[date.strftime("%I %p").lower()],
                                                    "color": "pink"}
    print(avg_dict)
    return avg_dict