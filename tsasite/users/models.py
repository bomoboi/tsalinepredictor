from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class AgentManager(BaseUserManager):
    def create_user(self, agent_id, agent_email, password=None):
        if not agent_email:
            raise ValueError("Agent must have an email address")
        elif not agent_id:
            raise ValueError("Agent must have a valid ID")

        agent = self.model(
            agent_id = agent_id,
            agent_email=self.normalize_email(agent_email),
        )

        agent.set_password(password)
        agent.save(using=self._db)
        return agent

    def create_superuser(self, agent_id, agent_email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        admin= self.create_user(
            agent_id,
            password=password,
            agent_email=agent_email,
        )
        admin.is_admin = True
        admin.save(using=self._db)
        return admin

class Agent(AbstractBaseUser, PermissionsMixin):
    agent_id = models.CharField(unique=True,
                                max_length = 8,
                                help_text="Format must Be T1234567",
                                validators=[
                                    RegexValidator(r'^(T\d{7})$')
                                ])
    agent_email = models.CharField(unique=True,
                                   max_length = 254,
                                   help_text="lastnamefirstinitiallast4ofid@tsa.gov",
                                   validators=[
                                       RegexValidator(r'^([a-zA-Z]{2,242}\d{4})@tsa\.gov$')
                                   ])

    USERNAME_FIELD = 'agent_id'
    EMAIL_FIELD = 'agent_email'
    REQUIRED_FIELDS = ['agent_email']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def get_short_name(self):
        return f"Agent {self.agent_id}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.agent_id

    @property
    def is_staff(self):
        return self.is_admin

    objects = AgentManager()
