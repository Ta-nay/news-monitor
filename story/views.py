import feedparser

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            story.save()
            form.save_m2m()
            return redirect("story_list")

    else:
        form = StoryForm()

    return render(request, "story/add_story.html", {"form": form})


def fetch_stories(user):
    sources = Source.objects.filter(company=user.company)

    for source in sources:
        feed_object = feedparser.parse(source.url)

        for entry in feed_object.entries:
            Story.objects.get_or_create(
                company=user.company,
                url=entry.link,
                defaults={
                    "title": entry.get("title", "")[:255],
                    "body_text": entry.get("description", ""),
                    "created_by": user,
                    "updated_by": user,
                    "source": source,
                },
            )


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    context_object_name = "stories"

    def get(self, request, *args, **kwargs):
        fetch_stories(request.user)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Story.objects.filter(company=self.request.user.company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = self.request.user.company

        context["sources"] = Source.objects.filter(
            company=company
        ).prefetch_related("story_sources")

        context["custom_stories"] = Story.objects.filter(
            company=company, source__isnull=True
        )

        return context


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
