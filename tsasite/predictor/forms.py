from django import forms
from django.core.validators import RegexValidator
from django.forms import DateTimeInput, IntegerField
from django.contrib.auth import authenticate, login
from .models import Record

INPUT_STYLES = " ".join(["background-color: rgba(0, 0, 0, 0.2);",
                         "border-bottom: 2px solid white;",
                         "padding: 2px;",
                         "text-align: center"])

FORM_STYLES = " ".join(["background-color: rgba(0, 0, 0, 0.2);",
                         "border-bottom: 2px solid white;",
                         "padding: 4px;",
                         "text-align: center"])
AP_LIST = {
    "ATL":  "ATL - Hartsfield-Jackson Atlanta International Airport",
    "DFW": "DFW - Dallas Fort Worth International Airport",
    "DEN": "DEN - Denver International Airport",
    "LAX": "LAX - Los Angeles International Airport",
    "ORD": "ORD - O'Hare International Airport",
    "JFK": "JFK - John F. Kennedy International Airport",
    "MCO": "MCO - Orlando International Airport",
    "LAS": "LAS - Harry Reid International Airport",
    "CLT": "CLT - Charlotte Douglas International Airport",
    "MIA": "MIA - Miami International Airport"
}

class AuthForm(forms.Form):
    agent_id = forms.CharField(label="",
                               max_length=8,
                               min_length=8,
                               validators = [
                                   RegexValidator(r'^(T\d{7})$')
                                ],
                               widget=forms.TextInput(attrs={"placeholder": "Agent ID",
                                                             "style": INPUT_STYLES}))

    # TODO validate passwords
    agent_password = forms.CharField(label="",
                                     max_length=64,
                                     min_length=8,
                                     widget=forms.PasswordInput(attrs={"placeholder": "Password",
                                                                       "style": INPUT_STYLES}))

    def clean(self):
        agent_id = self.cleaned_data.get("agent_id")
        agent_password = self.cleaned_data.get("agent_password")
        agent = authenticate(username=agent_id, password=agent_password)

        if not agent or not agent.is_active:
            raise forms.ValidationError("Invalid ID/Password combo")

        return self.cleaned_data

    def login(self, request):
        agent_id = self.cleaned_data.get("agent_id")
        agent_password = self.cleaned_data.get("agent_password")
        agent = authenticate(username=agent_id, password=agent_password)

        return agent

class UserForm(forms.Form):

    date = forms.DateTimeField(label="")

    date.widget.attrs.update({"placeholder": "Select a date and time",
                              "id": "dt-input",
                              "style": FORM_STYLES})
    ap = forms.ChoiceField(label="", choices=AP_LIST)

    ap.widget.attrs.update({"placeholder": "Select an airport",
                            "style": FORM_STYLES})



class SimForm(forms.Form):
    date = forms.DateTimeField(label="")

    date.widget.attrs.update({"placeholder": "Select a date and time",
                              "id": "dt-input",
                              "style": FORM_STYLES})

    ap = forms.ChoiceField(label="", choices=AP_LIST)

    ap.widget.attrs.update({"placeholder": "Select an airport",
                            "style": FORM_STYLES})

    num_agents = IntegerField(label="")

    num_agents.widget.attrs.update({"placeholder": "Input a number of agents",
                                    "style": FORM_STYLES})
