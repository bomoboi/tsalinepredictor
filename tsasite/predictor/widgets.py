from django import forms

AP_LIST = {
    "ATL - Hartsfield-Jackson Atlanta International Airport": "ATL",
    "DFW - Dallas Fort Worth International Airport": "DFW",
    "DEN - Denver International Airport": "DEN",
    "LAX - Los Angeles International Airport": "LAX",
    "ORD - O'Hare International Airport": "ORD",
    "JFK - John F. Kennedy International Airport": "JFK",
    "MCO - Orlando International Airport": "MCO",
    "LAS - Harry Reid International Airport": "LAS",
    "CLT - Charlotte Douglas International Airport": "CLT",
    "MIA - Miami International Airport": "MIA"
}

class APSelect(forms.Widget):
    def __init__(self, attrs=None):
        ap_list = AP_LIST
        widget = forms.Select(attrs=attrs, choices=ap_list)
        super().__init__(attrs)
