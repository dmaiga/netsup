from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sites.models import Site

from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def superviseur_sites(request):

    query = request.GET.get("q", "")

    sites = Site.objects.filter(actif=True)

    if query:
        sites = sites.filter(
            Q(nom__icontains=query) |
            Q(adresse__icontains=query)
        )

    sites = sites.order_by("nom")

    paginator = Paginator(sites, 12)  # 12 sites par page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sites/site.html",
        {
            "page_obj": page_obj,
            "query": query
        }
    )