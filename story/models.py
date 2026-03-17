from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import URLValidator
from django.db import models

from company.models import Company
from source.models import Source


# Create your models here.
class Story(models.Model):
    """This model is to store the stories fetched from the Source rss"""
    # ManyToMany
    tagged_companies = models.ManyToManyField(
        Company, related_name="story_tags"
    )

    # OneToMany
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        related_name="story_companies",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        null=True,
        related_name="story_sources",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="created_stories",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="updated_stories",
    )

    title = models.CharField(max_length=512)
    body_text = models.TextField()
    url = models.TextField(validators=[URLValidator()])

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "url")
        indexes = [
            GinIndex(
                fields=["title"],
                name="story_title_gin",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["body_text"],
                name="story_body_gin",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.title
