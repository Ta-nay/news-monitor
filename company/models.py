from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import URLValidator
from django.db import models


# Create your models here.
class Company(models.Model):
    """
    Company with a unique name and url.
    """
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

    name = models.CharField(max_length=256, unique=True)
    url = models.TextField(validators=[URLValidator()])

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "url")
        indexes = [
            GinIndex(
                fields=["name"],
                name="company_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["url"],
                name="company_url_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.name
