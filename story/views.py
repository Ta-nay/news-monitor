from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import StoryForm


@login_required
def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.updated_by = request.user
            story.save()

            form.save_m2m()

            return redirect("story_list")

    else:
        form = StoryForm()

    return render(request, "story/add_story.html", {"form": form})
