import feedparser

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from story.forms import StoryForm
from story.models import Story
from source.models import Source
from story.service import (
    fetch_stories,
    save_story_instance,
    get_stories_for_user,
    delete_story_service,
)


@login_required
def add_or_update(request, id=None):
    story = None
    if id:
        try:
            story = get_stories_for_user(request.user, None).get(id=id)
        except ObjectDoesNotExist:
            return redirect("story_list")
    if request.method == "POST":
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            save_story_instance(form, request.user)
            return redirect("story_list")
    else:
        form = StoryForm(instance=story)
    return render(request, "story/add_story.html", {"form": form})


@login_required
def list_story(request):
    company_id = request.user.company_id
    cache_key = f"rss_fetch_{company_id}"
    if not cache.get(cache_key):
        fetch_stories(request.user)
        cache.set(cache_key, True, 600)
    query = request.GET.get("q")
    query_params = request.GET.copy()
    query_params.pop("page", None)
    stories_qs = get_stories_for_user(request.user, query)
    # pagination logic
    page_number = request.GET.get("page")
    stories = Paginator(stories_qs, 25).get_page(page_number)
    return render(
        request,
        "story/story_list.html",
        {
            "stories": stories,
            "page_obj": stories,
            "query_params": query_params.urlencode(),
        },
    )


@login_required
@require_POST
def delete_story(request, id):
    delete_story_service(request.user, id)
    return redirect("story_list")


# class StoryDeleteView(LoginRequiredMixin, DeleteView):
#     model = Story
#     template_name = "story/delete_story.html"
#     success_url = reverse_lazy("story_list")
#
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Story.objects.all()
#         return Story.objects.filter(company=self.request.user.company)
#
#
# class StoryListView(LoginRequiredMixin, ListView):
#     model = Story
#     paginate_by = 25
#     context_object_name = "stories"
#     template_name = "story/story_list.html"
#
#     def get(self, request, *args, **kwargs):
#         """ This method is called when the story list page is requested."""
#         company_id = request.user.company_id
#         cache_key = f"rss_fetch_{company_id}"
#         if not cache.get(cache_key):
#             fetch_stories(request.user)
#             cache.set(cache_key, True, 600)
#         return super().get(request, *args, **kwargs)
#
#     def get_queryset(self):
#         """ A custom queryset to return the stories that belong to the company of the logged in user. """
#         if self.request.user.is_staff:
#             return Story.objects.all()
#         queryset = (
#             Story.objects.filter(company_id=self.request.user.company_id)
#             .select_related("source","created_by")
#             .prefetch_related("tagged_companies")
#             .order_by("-id")
#         )
#         query = self.request.GET.get("q")
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) | Q(body_text__icontains=query)
#             )
#         return queryset
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #
#     #     company = self.request.user.company
#     #
#     #     context["sources"] = Source.objects.filter(
#     #         company=company
#     #     ).prefetch_related(
#     #         Prefetch(
#     #             "story_sources",
#     #             queryset=Story.objects.select_related(
#     #                 "source"
#     #             ).prefetch_related("tagged_companies"),
#     #         )
#     #     )
#     #
#     #     context["custom_stories"] = Story.objects.filter(
#     #         company=company,
#     #         source__isnull=True,
#     #     ).prefetch_related("tagged_companies")
#     #
#     #     return context


# class StoryUpdateView(LoginRequiredMixin, UpdateView):
#     model = Story
#     fields = ["title", "body_text", "url", "tagged_companies"]
#     template_name = "story/edit_story.html"
#     success_url = reverse_lazy("story_list")
#
#     def get_queryset(self):
#         return Story.objects.filter(company=self.request.user.company)

# def story_autocomplete(request):
#     """ Logic to add autocomplete for story searching bar. """
#     query = request.GET.get("q", "")
#     stories = Story.objects.filter(title__icontains=query).values(
#         "title", "url"
#     )[:5]
#     return JsonResponse({"results": list(stories)})
