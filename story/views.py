from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .forms import StoryForm
from .models import Story


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


class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    context_object_name = "stories"

    def get_queryset(self):
        return Story.objects.filter(created_by=self.request.user)
