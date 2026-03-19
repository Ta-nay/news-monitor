from django.db.models import Q

from source.models import Source


def get_sources_queryset(user, query=None):
    query_dict = {"company_id": user.company_id}
    if user.is_staff:
        queryset = Source.objects.all()
    else:
        queryset = Source.objects.filter(**query_dict)
    queryset = queryset.select_related(
        "company", "created_by", "updated_by"
    ).prefetch_related("tagged_companies")
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(url__icontains=query)
        )
    return queryset.order_by("-created_on")


def save_source_service(form, user):
    """Handle saving logic for Source."""
    source = form.save(commit=False)
    if not source.id:
        source.created_by = user
        source.company = user.company
    source.updated_by = user
    source.save()
    form.save_m2m()
    return source


def delete_source_service(user, id):
    qd = {"id": id}
    if not user.is_staff:
        qd["created_by_id"] = user.id
    src = Source.objects.filter(**qd).delete()


# def delete_source_for_user(user, pk):
#     """Delete source with permission check."""
#     query_dict = {
#         "pk": pk,
#     }
#     source = get_source_for_user(user).get(**query_dict)
#     source.delete()
