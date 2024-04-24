from django.forms import ModelForm, CharField, PasswordInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Agent

class AgentCreationForm(ModelForm):

    password = CharField(label="Password",
                         widget=PasswordInput)

    confirm_pass = CharField(label="Password Confirmation",
                             widget=PasswordInput)

    class Meta:
        model = Agent
        fields = ("agent_id", "agent_email")

    def checkPassword(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('confirm_pass')

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Passwords do not match")

        return pass2

    def save(self, commit=True):
        agent = super().save(commit=False)
        agent.set_password(self.cleaned_data["password"])

        if commit:
            agent.save()

        return agent


class AgentChangeForm(ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Agent
        fields = ["agent_id", "agent_email", "is_active", "is_admin"]


