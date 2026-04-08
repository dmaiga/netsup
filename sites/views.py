from urllib import request

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sites.models import Site,AffectationAgent
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SiteForm

from controles.models import ControleSite

from users.models import User,Technicien

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from controles.models import ControleSite

from django.db.models import Count, Sum
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from django.core.paginator import Paginator


from django.db.models import Avg, FloatField, ExpressionWrapper, F


@login_required
def superviseur_sites(request):

    query = request.GET.get("q", "")

    sites = Site.objects.filter(actif=True,superviseur=request.user)

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


@login_required
def admin_site_create(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_site_list')
    else:
        form = SiteForm()

    return render(request, 'sites/admin_create.html', {'form': form})


from django.db.models import Count, Q

@login_required
def admin_site_list(request):
    # Récupération des filtres
    q_site = request.GET.get('q_site', '')
    q_client = request.GET.get('q_client', '')
    q_superviseur = request.GET.get('q_superviseur', '')

    # 1. On prépare la requête de base avec l'annotation
    sites_list = Site.objects.all().annotate(
        nb_tech_reels=Count('affectations', filter=Q(affectations__actif=True))
    ).select_related('superviseur') # Optimisation pour éviter des requêtes SQL en boucle

    # 2. Application des filtres
    if q_superviseur:
        sites_list = sites_list.filter(superviseur_id=q_superviseur)
    if q_site:
        sites_list = sites_list.filter(nom__icontains=q_site)
    if q_client:
        sites_list = sites_list.filter(client_nom__icontains=q_client)

    sites_list = sites_list.order_by('nom')

    # 3. Récupération de tous les superviseurs pour le filtre (Dropdown)
    # On ne prend que ceux qui sont liés à au moins un site pour rester propre
    liste_superviseurs = User.objects.filter(role="superviseur").order_by('first_name')

    paginator = Paginator(sites_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sites/admin_list.html', {
        'page_obj': page_obj,
        'q_site': q_site,
        'q_client': q_client,
        'q_superviseur': q_superviseur,
        'liste_superviseurs': liste_superviseurs,
    })

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

@login_required
def admin_site_detail(request, pk):
    site = get_object_or_404(Site.objects.select_related('superviseur'), pk=pk)
    
    # Initialisation des variables de contrôle
    nb_visites_semaine = 0
    est_regulier = False
    historique_superviseur = []

    # On ne calcule la performance que si un superviseur est assigné
    if site.superviseur:
        une_semaine_ago = timezone.now() - timedelta(days=7)
        nb_visites_semaine = site.controlesite_set.filter(
            superviseur=site.superviseur,
            date__gte=une_semaine_ago
        ).count()
        
        est_regulier = nb_visites_semaine >= 2
        
        # Historique spécifique du superviseur assigné
        historique_superviseur = site.controlesite_set.filter(
            superviseur=site.superviseur
        ).order_by('-date')[:15]
    else:
        # Optionnel : si pas de superviseur attitré, on montre les derniers contrôles globaux
        historique_superviseur = site.controlesite_set.all().order_by('-date')[:15]


    # Gestion des agents
    affectations = AffectationAgent.objects.filter(site=site).select_related('technicien').order_by('-actif')
    ids_deja_presents = affectations.values_list('technicien_id', flat=True)
    
    # On prend les techniciens actifs qui ne sont pas dans la liste ci-dessus
    techniciens_disponibles = Technicien.objects.filter(
        actif=True
    ).exclude(
        id__in=ids_deja_presents
    ).order_by('nom')
    if request.method == 'POST':
        if 'nb_prevus' in request.POST:
            site.nombre_techniciens_prevus = request.POST.get('nb_prevus')
            site.superviseur_id = request.POST.get('superviseur_id')
            site.actif = 'actif' in request.POST
            site.save()
            messages.success(request, "Site mis à jour.")
            return redirect('admin_site_detail', pk=site.id)

    # Pour le menu déroulant des superviseurs
    tous_superviseurs = User.objects.filter(role='superviseur', is_active=True)

    return render(request, 'sites/admin_detail.html', {
        'site': site,
        'affectations': affectations,
        'techniciens_disponibles': techniciens_disponibles,
        'historique_superviseur': historique_superviseur,
        'nb_visites_semaine': nb_visites_semaine,
        'est_regulier': est_regulier,
        'tous_superviseurs': tous_superviseurs,
    })

@login_required
def gestion_affectations(request, site_id):
    """
    Vue direction : ajouter / retirer / réactiver un agent sur un site.
    Remplace l'ancienne logique FK par AffectationAgent M2M.
    """
    site = get_object_or_404(Site, pk=site_id)
    affectations = AffectationAgent.objects.filter(site=site).select_related('technicien').order_by('-actif', 'technicien__nom')

    # Techniciens pas encore affectés à ce site
    techniciens_deja = affectations.values_list('technicien_id', flat=True)
    disponibles = Technicien.objects.filter(actif=True).exclude(id__in=techniciens_deja).order_by('nom')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'affecter':
            tech_id = request.POST.get('technicien_id')
            tech = get_object_or_404(Technicien, id=tech_id)
            aff, created = AffectationAgent.objects.get_or_create(
                technicien=tech, site=site,
                defaults={'actif': True}
            )
            if not created:
                aff.actif = True
                aff.date_fin = None
                aff.save()
            messages.success(request, f"{tech} affecté(e) à {site.nom}.")

        elif action == 'retirer':
            aff_id = request.POST.get('affectation_id')
            aff = get_object_or_404(AffectationAgent, id=aff_id, site=site)
            from django.utils import timezone as tz
            import datetime
            aff.actif = False
            aff.date_fin = tz.now().date()
            aff.save()
            messages.info(request, f"{aff.technicien} retiré(e) de {site.nom}.")

        return redirect('gestion_affectations', site_id=site_id)

    return render(request, 'sites/admin_detail.html', {
        'site': site,
        'affectations': affectations,
        'techniciens_disponibles': disponibles,
        'vue_affectations': True, 
    })


