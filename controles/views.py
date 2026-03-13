from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from controles.forms import ControleSiteForm
from controles.models import ControleSite
from sites.models import Site
from django.contrib import messages
@login_required
def controle_site(request, site_id):
    # 1. On récupère le site
    site = get_object_or_404(Site, id=site_id)

    if request.method == "POST":
        # 2. IMPORTANT : On passe l'objet 'site' au formulaire pour la validation
        # du nombre de techniciens (clean method)
        form = ControleSiteForm(request.POST, request.FILES, site=site)

        if form.is_valid():
            controle = form.save(commit=False)

            # 3. Attribution des données liées
            controle.site = site
            controle.superviseur = request.user

            # 4. Calcul automatique des effectifs
            # On utilise le champ du modèle Site
            controle.techniciens_prevus = site.nombre_techniciens_prevus
            
            # Calcul des absents (sécurisé par le formulaire qui empêche presents > prevus)
            controle.techniciens_absents = site.nombre_techniciens_prevus - controle.techniciens_presents

            # 5. Récupération des coordonnées GPS (envoyées par JS dans le template)
            controle.gps_lat = request.POST.get("gps_lat")
            controle.gps_long = request.POST.get("gps_long")

            controle.save()

            # Message de succès (Optionnel mais recommandé)
            messages.success(request, f"Contrôle enregistré pour {site.nom}")

            return redirect("superviseur_sites")
    else:
        # Initialisation du formulaire vide avec le site
        form = ControleSiteForm(site=site)

    return render(
        request,
        "controle/form.html",
        {
            "form": form,
            "site": site
        }
    )
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

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

    # Pagination : 10 éléments par page
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

    return render(
        request,
        "controle/controle_detail.html",
        {"controle": controle}
    )

@login_required
def scan(request):

    return render(
        request,
        "controle/scan.html",

    )
