from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from source.forms import SourceForm
from source.models import Source
from source.service import (
    get_sources_queryset,
    save_source_service,
    delete_source_service,
)
from story.service import fetch_stories


# Create your views here.
@login_required
def add_or_update(request, id=None):
    """A combined view to add and update sources."""
    source = None
    if id:
        try:
            source = get_sources_queryset(request.user, None).get(id=id)
        except ObjectDoesNotExist:
            return redirect("source_list")
    if request.method == "POST":
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            save_source_service(form, request.user)
            fetch_stories(request.user)
            return redirect("source_list")
    else:
        form = SourceForm(instance=source)
    return render(request, "source/add_source.html", {"form": form})


@login_required
def list_source(request):
    query = request.GET.get("q")
    queryset = get_sources_queryset(request.user, query)
    page_number = request.GET.get("page")
    query_params = request.GET.copy()
    query_params.pop("page", None)
    page_obj = Paginator(queryset, 4).get_page(page_number)
    return render(
        request,
        "source/source_list.html",
        {
            "page_obj": page_obj,
            "sources": page_obj,
            "query_params": query_params.urlencode(),
        },
    )


@login_required
@require_POST
def delete_source(request, id):
    delete_source_service(request.user, id)
    return redirect("source_list")

# def source_autocomplete(request):
#     """Logic for autocomplete added on source searching bar."""
#     query = request.GET.get("q", "")
#     sources = Source.objects.filter(name__icontains=query).values(
#         "name", "url"
#     )[:5]
#     return JsonResponse({"results": list(sources)})


# class SourceListView(LoginRequiredMixin, ListView):
#     model = Source
#     paginate_by = 10
#     context_object_name = "sources"
#
#     def get_queryset(self):
#         """A custom queryset that returns Sources that belong to the requesting users company."""
#
#         qd = { }
#         if query := self.request.GET.get("q"):
#            qd["name__icontains"] = query
#
#         if not self.request.user.is_staff:
#             qd["company_id"] = self.request.user.company_id
#
#         if self.request.user.is_staff:
#             return Source.objects.all()
#
#         return (
#             Source.objects.filter(**qd)
#             .select_related("company", "created_by", "updated_by")
#             .prefetch_related("tagged_companies")
#         )
#
#         # Todo: handle pagination logic
#         query = self.request.GET.get("q")
#         if query:
#             queryset = queryset.filter(
#                 Q(name__icontains=query) | Q(url__icontains=query)
#             )
#         return queryset


# class SourceDeleteView(LoginRequiredMixin, DeleteView):
#     model = Source
#     template_name = "source/delete_source.html"
#     success_url = reverse_lazy("source_list")
#
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Source.objects.all()
#         return Source.objects.filter(
#             company=self.request.user.company, created_by=self.request.user
#         )


# class SourceUpdateView(LoginRequiredMixin, UpdateView):
#     model = Source
#     fields = ["name", "url", "tagged_companies"]
#     template_name = "source/edit_source.html"
#     success_url = reverse_lazy("source_list")
#
#     def get_queryset(self):
#         return Source.objects.filter(company=self.request.user.company)
