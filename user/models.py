from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from company.models import Company

# Create your models here.


class Subscriber(AbstractUser):
    """A Subscriber model that inherits the Abstract user model, hence has access to fields -
    username, first_name, last_name, email, password which can be directly be accessed in forms.
    """

    # OneToMany
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="subscriber_companies",
        null=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_subscribers",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_subscribers",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
