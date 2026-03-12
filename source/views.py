from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Source
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
            source.company = request.user.company
            source.save()
            form.save_m2m()
            return redirect("source_list")

    else:
        form = SourceForm()

    return render(request, "source/add_source.html", {"form": form})


class SourceListView(LoginRequiredMixin, ListView):
    model = Source
    context_object_name = "sources"

    def get_queryset(self):
        return Source.objects.filter(created_by=self.request.user)


class SourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Source
    fields = ["name", "url", "tagged_companies"]
    template_name = "source/edit_source.html"
    success_url = reverse_lazy("source_list")

    def get_queryset(self):
        return Source.objects.filter(company=self.request.user.company)


class SourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Source
    template_name = "source/delete_source.html"
    success_url = reverse_lazy("source_list")

    def get_queryset(self):
        return Source.objects.filter(company=self.request.user.company)
