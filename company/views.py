from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from company.forms import CompanyForm
from company.models import Company


# Create your views here.
@login_required
def add_company(request):

    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.updated_by = request.user
            company.save()

    else:
        form = CompanyForm()

    return render(request, "company/add_company.html", {"form": form})


def company_autocomplete(request):
    term = request.GET.get("term", "")

    companies = Company.objects.filter(name__icontains=term)[:20]

    results = [{"id": c.id, "text": c.name} for c in companies]

    return JsonResponse({"results": results})
