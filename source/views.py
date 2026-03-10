from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import SourceForm

# Create your views here.


@login_required
def add_source(request):

    if request.method == "POST":
        form = SourceForm(request.POST)

        if form.is_valid():
            source = form.save(commit=False)
            source.created_by = request.user
            source.updated_by = request.user
            source.save()
            form.save_m2m()

    else:
        form = SourceForm()

    return render(request, "source/add_source.html", {"form": form})
