import feedparser

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Prefetch
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from .forms import StoryForm
from .models import Story
from source.models import Source


@login_required
def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.updated_by = request.user
            story.company = request.user.company
            try:
                story.save()
                form.save_m2m()
                return redirect("story_list")
            except IntegrityError:
                return HttpResponse("Integrity error: this URL already exists")

    else:
        form = StoryForm()

    return render(request, "story/add_story.html", {"form": form})


def fetch_stories(user):
    company_id = user.company_id

    sources = Source.objects.filter(company_id=company_id).only("id", "url")

    existing_urls = set(
        Story.objects.filter(company_id=company_id).values_list(
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
                    company_id=company_id,
                    url=url,
                    title=entry.get("title", "")[:255],
                    body_text=entry.get("description", ""),
                    created_by=user,
                    updated_by=user,
                    source_id=source.id,
                )
            )

            existing_urls.add(url)

    if new_stories:
        Story.objects.bulk_create(new_stories, batch_size=100)

        cache.delete(f"stories_{company_id}")


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    paginate_by = 25
    context_object_name = "stories"
    template_name = "story/story_list.html"

    def get(self, request, *args, **kwargs):
        company_id = request.user.company_id
        cache_key = f"rss_fetch_{company_id}"

        if not cache.get(cache_key):
            fetch_stories(request.user)
            cache.set(cache_key, True, 600)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Story.objects.filter(company_id=self.request.user.company_id)
            .select_related("source")
            .prefetch_related("tagged_companies")
            .order_by("-id")
        )

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     company = self.request.user.company
    #
    #     context["sources"] = Source.objects.filter(
    #         company=company
    #     ).prefetch_related(
    #         Prefetch(
    #             "story_sources",
    #             queryset=Story.objects.select_related(
    #                 "source"
    #             ).prefetch_related("tagged_companies"),
    #         )
    #     )
    #
    #     context["custom_stories"] = Story.objects.filter(
    #         company=company,
    #         source__isnull=True,
    #     ).prefetch_related("tagged_companies")
    #
    #     return context


class StoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Story
    fields = ["title", "body_text", "url", "tagged_companies"]
    template_name = "story/edit_story.html"
    success_url = reverse_lazy("story_list")

    def get_queryset(self):
        return Story.objects.filter(company=self.request.user.company)


class StoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Story
    template_name = "story/delete_story.html"
    success_url = reverse_lazy("story_list")

    def get_queryset(self):
        return Story.objects.filter(company=self.request.user.company)
