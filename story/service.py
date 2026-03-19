import feedparser

from django.core.cache import cache
from django.db.models import Q

from story.models import Story
from source.models import Source


def fetch_stories(user):
    """function to fetch stories from each source rss and cache them"""
    if user.is_staff:
        sources = Source.objects.all().only("id", "url", "company_id")
    else:
        sources = Source.objects.filter(company_id=user.company_id).only(
            "id", "url", "company_id"
        )
    # Load all existing story URLs once
    existing_urls = set(
        Story.objects.values_list("url", flat=True)
        if user.is_staff
        else Story.objects.filter(company_id=user.company_id).values_list(
            "url", flat=True
        )
    )
    new_stories = []
    for source in sources:
        feed = feedparser.parse(source.url)
        for entry in feed.entries[:10]:
            url = entry.get("link")
            if not url or url in existing_urls:
                continue
            new_stories.append(
                Story(
                    company_id=source.company_id,
                    url=url,
                    title=entry.get("title", "")[:512],
                    body_text=entry.get("description", ""),
                    created_by=source.created_by,
                    updated_by=source.created_by,
                    source_id=source.id,
                )
            )
            existing_urls.add(url)
    if new_stories:
        Story.objects.bulk_create(new_stories, batch_size=100)
        # Clear cache for affected companies
        company_ids = {story.company_id for story in new_stories}
        for cid in company_ids:
            cache.delete(f"stories_{cid}")


def get_stories_for_user(user, query=None):
    query_dict = {"company_id": user.company_id}
    if user.is_staff:
        queryset = (
            Story.objects.all()
            .select_related("company")
            .prefetch_related("tagged_companies")
        )
    else:
        queryset = (
            Story.objects.filter(**query_dict)
            .select_related("source", "created_by")
            .prefetch_related("tagged_companies")
        )
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(body_text__icontains=query)
        )
    return queryset.order_by("-id")


def save_story_instance(form, user):
    story = form.save(commit=False)
    if not story.id:
        story.created_by = user
        story.company = user.company
    story.updated_by = user
    story.save()
    form.save_m2m()
    return story


def delete_story_service(user, id):
    qd = {"id": id}
    if not user.is_staff:
        qd["created_by_id"] = user.id
    src = Story.objects.filter(**qd).delete()
