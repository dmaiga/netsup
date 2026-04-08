from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

from controles.forms import ControleSiteForm, build_pointage_formset
from controles.models import ControleSite, PointageAgent
from sites.models import Site

from users.models import User,Technicien


@login_required
def controle_site(request, site_id):
    site = get_object_or_404(Site, id=site_id, superviseur=request.user)

    # Agents actuellement affectés à ce site (via AffectationAgent M2M)
    agents = site.get_agents_actifs()


    if request.method == "POST":
        form = ControleSiteForm(request.POST, request.FILES, site=site)
        pointage_formset = build_pointage_formset(agents, data=request.POST)

        if form.is_valid() and pointage_formset.is_valid():
            # Calcul du nombre présents depuis le pointage nominal
            nb_presents = sum(
                1 for f in pointage_formset
                if f.cleaned_data.get("present")
            )
            nb_prevus = site.nombre_techniciens_prevus or agents.count()

            controle = form.save(commit=False)
            controle.site = site
            controle.superviseur = request.user
            controle.techniciens_prevus = nb_prevus
            controle.techniciens_presents = nb_presents
            controle.techniciens_absents = nb_prevus - nb_presents
            controle.gps_lat = request.POST.get("gps_lat") or None
            controle.gps_long = request.POST.get("gps_long") or None
            controle.save()

            # Sauvegarde des pointages nominaux
            for f in pointage_formset:
                cd = f.cleaned_data
                tech_id = cd.get("technicien_id")
                if not tech_id:
                    continue
                try:
                    tech = Technicien.objects.get(id=tech_id)
                except Technicien.DoesNotExist:
                    continue
                PointageAgent.objects.create(
                    controle=controle,
                    technicien=tech,
                    present=cd.get("present", False),
                    motif_absence=cd.get("motif_absence", ""),
                    commentaire=cd.get("commentaire", ""),
                )

            messages.success(request, f"Contrôle enregistré pour {site.nom} — {nb_presents} présent(s) sur {nb_prevus} prévu(s).")
            return redirect("superviseur_sites")

    else:
        form = ControleSiteForm(site=site)
        pointage_formset = build_pointage_formset(agents)

    return render(
        request,
        "controle/form.html",
        {
            "form": form,
            "site": site,
            "agents": agents,
            "pointage_formset": pointage_formset,
        }
    )


@login_required
def controle_list(request):
    controles_list = ControleSite.objects.filter(superviseur=request.user)

    filtre = request.GET.get('filter')
    if filtre == 'incidents':
        controles_list = controles_list.filter(incident=True)
    elif filtre == 'semaine':
        une_semaine_ago = timezone.now() - timedelta(days=7)
        controles_list = controles_list.filter(date__gte=une_semaine_ago)

    controles_list = controles_list.order_by("-date")

    paginator = Paginator(controles_list, 10)
    page_number = request.GET.get('page')
    controles = paginator.get_page(page_number)

    return render(
        request,
        "controle/controle_list.html",
        {
            "controles": controles,
            "current_filter": filtre
        }
    )


@login_required
def controle_detail(request, pk):
    controle = get_object_or_404(
        ControleSite,
        pk=pk,
        superviseur=request.user
    )
    pointages = controle.pointages.select_related('technicien').order_by('technicien__nom')

    return render(
        request,
        "controle/controle_detail.html",
        {
            "controle": controle,
            "pointages": pointages,
        }
    )


@login_required
def scan(request):
    return render(request, "controle/scan.html")


def scan_redirect(request, site_id):
    if not request.user.is_authenticated:
        from django.urls import reverse
        return redirect(f"/login/?next={reverse('controle_site', kwargs={'site_id': site_id})}")
    return redirect("controle_site", site_id=site_id)
