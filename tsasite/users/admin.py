from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import AgentCreationForm, AgentChangeForm
from .models import Agent
# Register your models here.
class AdminAgent(UserAdmin):

    form = AgentChangeForm
    add_form = AgentCreationForm

    list_display = ["agent_id", "agent_email", "is_admin"]

    list_filter = ["is_admin"]

    search_fields = ["agent_id"]
    ordering = ["agent_email"]
    filter_horizontal = []

    fieldsets = [
        (None, {"fields": ["agent_id", "agent_email", "password"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["agent_id","agent_email", "password", "confirm_pass"],
            },
        ),
    ]

admin.site.register(Agent, AdminAgent)
admin.site.unregister(Group)
