from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import URLValidator
from django.db import models

from company.models import Company


# Create your models here.
class Source(models.Model):
    """
    Source model for adding a unique source rss, each source must be unique for the company
    """
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

    name = models.CharField(max_length=256)
    url = models.TextField(validators=[URLValidator()])

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "url")
        indexes = [
            GinIndex(
                fields=["name"],
                name="source_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["url"],
                name="source_url_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.name
