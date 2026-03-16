from django.conf import settings
from django.core.validators import URLValidator
from django.db import models

from company.models import Company


# Create your models here.
class Source(models.Model):
    # ManyToMany
    tagged_companies = models.ManyToManyField(
        Company, related_name="source_tags"
    )

    # OneToMany
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="source_companies"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="created_sources",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="update_sources",
    )

    name = models.CharField(max_length=256, db_index=True)
    url = models.URLField(db_index=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "url")
        # indexes = [
        #     models.Index(fields=["name"]),
        # ]

    def __str__(self):
        return self.name
