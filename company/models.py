from django.conf import settings
from django.core.validators import URLValidator
from django.db import models


# Create your models here.
class Company(models.Model):
    # OneToMany
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_companies",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_companies",
    )

    name = models.CharField(max_length=256)
    url = models.URLField(validators=[URLValidator()])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
