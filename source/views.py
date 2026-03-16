from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import  Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView,  DeleteView

from .models import Source
from .forms import SourceForm

# Create your views here.
def source_autocomplete(request):
    query = request.GET.get("q", "")
    sources = (
        Source.objects
        .filter(name__icontains=query)
        .values("name", "url")[:5]
    )
    return JsonResponse({
        "results": list(sources)
    })


@login_required
def save_source(request, pk=None):
    if pk:
        if request.user.is_staff:
            # Admin can edit any company source
            source = get_object_or_404(
                Source,
                pk=pk,
                company=request.user.company
            )
        else:
            # Normal users can edit only their own sources
            source = get_object_or_404(
                Source,
                pk=pk,
                company=request.user.company,
                created_by=request.user
            )
    else:
        source = None

    if request.method == "POST":
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            source = form.save(commit=False)
            if not source.pk:
                source.created_by = request.user
                source.company = request.user.company
            source.updated_by = request.user
            source.save()
            form.save_m2m()
            return redirect("source_list")
    else:
        form = SourceForm(instance=source)
    return render(request, "source/add_source.html", {"form": form})


class SourceListView(LoginRequiredMixin, ListView):
    model = Source
    context_object_name = "sources"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Source.objects.all()
        queryset = Source.objects.filter(company=self.request.user.company)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(url__icontains=query)
            )
        return queryset


# class SourceUpdateView(LoginRequiredMixin, UpdateView):
#     model = Source
#     fields = ["name", "url", "tagged_companies"]
#     template_name = "source/edit_source.html"
#     success_url = reverse_lazy("source_list")
#
#     def get_queryset(self):
#         return Source.objects.filter(company=self.request.user.company)


class SourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Source
    template_name = "source/delete_source.html"
    success_url = reverse_lazy("source_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Source.objects.all()
        return Source.objects.filter(
            company=self.request.user.company,
            created_by=self.request.user
        )
