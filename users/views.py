from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 

from sites.models import Site
from controles.models import ControleSite

from users.models import User
from users.forms import UserForm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from controles.models import ControleSite
from sites.models import Site,Technicien
from django.db.models import Count, Sum
from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta


def redirect_dashboard(user):

    if user.role == "superviseur":
        return "dashboard_superviseur"

    if user.role in ["admin", "direction"]:
        return "dashboard_admin"

    return "login"

def login_view(request):

    if request.method == "POST":

        telephone = request.POST.get("telephone")
        password = request.POST.get("password")

        user = authenticate(request, telephone=telephone, password=password)

        if user is not None:

            if not user.is_active:
                messages.error(request, "Compte désactivé")
                return redirect("login")

            login(request, user)

            return redirect(redirect_dashboard(user))

        else:
            messages.error(request, "Téléphone ou mot de passe incorrect")

    return render(request, "users/auth/login.html")


def logout_view(request):

    logout(request)

    return redirect("login")




@login_required
def dashboard_superviseur(request):

    total_sites = Site.objects.filter(actif=True).count()

    total_controles = ControleSite.objects.filter(
        superviseur=request.user
    ).count()

    last_controles = ControleSite.objects.filter(
        superviseur=request.user
    ).order_by("-date")[:5]

    context = {

        "total_sites": total_sites,
        "total_controles": total_controles,
        "last_controles": last_controles

    }

    return render(request, "users/dashboard/superviseur.html",context)


from django.core.paginator import Paginator
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain
from django.core.paginator import Paginator

@login_required
def user_list(request):
    query = request.GET.get('q', '')
    
    # 1. Superviseurs (Uniquement ceux qui ne sont pas Direction/Admin)
    users_qs = User.objects.filter(is_deleted=False, is_superuser=False).order_by('last_name')
    
    # 2. Techniciens (Terrain)
    techs_qs = Technicien.objects.filter(actif=True).order_by('nom')

    if query:
        users_qs = users_qs.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        techs_qs = techs_qs.filter(Q(nom__icontains=query) | Q(prenom__icontains=query))

    # Pagination des techniciens (car ils seront les plus nombreux)
    paginator_techs = Paginator(techs_qs, 10) 
    page_techs = request.GET.get('page_techs')
    techs_obj = paginator_techs.get_page(page_techs)

    return render(request, "users/user/list.html", {
        "users": users_qs, # Liste courte des superviseurs
        "techs": techs_obj, # Liste paginée des techniciens
        "query": query
    })

def user_detail(request, pk):

    user = get_object_or_404(User, pk=pk)

    return render(request, "users/user/detail.html", {
        "user": user
    })


def user_create(request):

    if request.method == "POST":

        form = UserForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            return redirect("user_list")

    else:

        form = UserForm()

    return render(request, "users/user/create.html", {"form": form})
 
def user_update(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            return redirect("user_list")

    else:

        form = UserForm(instance=user)

    return render(request, "users/user/create.html", {
        "form": form,
        "user": user
    })

 
def user_toggle_active(request, pk):

    user = User.objects.get(pk=pk)

    user.is_active = not user.is_active

    user.save()

    return redirect("user_list")
 
def user_soft_delete(request, pk):

    user = User.objects.get(pk=pk)

    user.is_deleted = True
    user.is_active = False

    user.save()

    return redirect("user_list")

 

# Créer un technicien (Globalement, sans obligation de site)
@login_required
def technicien_create(request):
    if request.method == "POST":
        Technicien.objects.create(
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            telephone=request.POST.get('telephone'),
            type_contrat=request.POST.get('type_contrat'),
            photo=request.FILES.get('photo'),
            actif=True
        )
        return redirect('user_list') # Retourne à ta liste unique
    
    return render(request, "users/user/tech_form.html")

# Modifier un technicien
@login_required
def technicien_update(request, pk):
    tech = get_object_or_404(Technicien, pk=pk)
    
    if request.method == "POST":
        tech.nom = request.POST.get('nom')
        tech.prenom = request.POST.get('prenom')
        tech.telephone = request.POST.get('telephone')
        tech.type_contrat = request.POST.get('type_contrat')
        
        if request.FILES.get('photo'):
            tech.photo = request.FILES.get('photo')
            
        tech.save()
        return redirect('user_list')
    
    return render(request, "users/user/tech_form.html", {"tech": tech})


# Désactiver un technicien (Soft Delete)
@login_required
def technicien_soft_delete(request, pk):
    tech = get_object_or_404(Technicien, pk=pk)
    tech.actif = False
    tech.save()
    return redirect('user_list')

@login_required
def technicien_detail(request, pk):
    tech = get_object_or_404(Technicien, pk=pk)
    # On récupère le site actuel s'il existe
    site_actuel = getattr(tech, 'site', None) 
    
    return render(request, "users/user/tech_detail.html", {
        "tech": tech,
        "site_actuel": site_actuel
    })


@login_required
def dashboard_direction(request):
    # --- Période de la semaine ---
    aujourd_hui = timezone.now()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    # On définit la fin de semaine (Dimanche soir)
    fin_semaine = debut_semaine + timedelta(days=6, hours=23, minutes=59)

    # --- Données de base ---
    total_sites = Site.objects.filter(actif=True).count()
    controles_semaine = ControleSite.objects.filter(date__gte=debut_semaine)
    total_controles_hebdo = controles_semaine.count()
    
    # Objectif : 2 contrôles par site par semaine
    objectif_hebdo = total_sites * 2
    # Calcul du % de couverture global de la semaine
    progression_hebdo = (total_controles_hebdo / objectif_hebdo * 100) if objectif_hebdo > 0 else 0

    # --- Statistiques Globales (Toute période) ---
    controles_all = ControleSite.objects.all()
    stats_tech = controles_all.aggregate(
        presents=Sum("techniciens_presents"),
        absents=Sum("techniciens_absents")
    )
    
    # --- Incidents & Alertes ---
    # Uniquement ceux qui ne sont pas encore résolus
    incidents_actifs = ControleSite.objects.filter(
        incident=True, 
        incident_resolu=False
    ).select_related('site', 'superviseur').order_by('-date')

    # Sites à surveiller (Mauvaise note de propreté sur le dernier contrôle)
    # On limite à 5 pour ne pas surcharger le dashboard
    sites_critiques = ControleSite.objects.filter(
        etat_proprete='mauvais'
    ).select_related('site').order_by('-date')[:5]

    context = {
        "debut_semaine": debut_semaine,
        "fin_semaine": fin_semaine,
        "aujourd_hui": aujourd_hui,
        "total_sites": total_sites,
        "total_controles_hebdo": total_controles_hebdo,
        "objectif_hebdo": objectif_hebdo,
        "progression_hebdo": round(progression_hebdo, 1),
        "techniciens_presents": stats_tech['presents'] or 0,
        "techniciens_absents": stats_tech['absents'] or 0,
        "incidents_actifs": incidents_actifs,
        "total_incidents_actifs": incidents_actifs.count(),
        "sites_critiques": sites_critiques,
    }
    return render(request, "users/dashboard/admin.html", context)


@login_required
def couverture_hebdo(request):
    aujourd_hui = timezone.now()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    
    # Recherche par nom de site ou client
    query = request.GET.get('q', '')
    sites_list = Site.objects.filter(actif=True).order_by('nom')
    if query:
        sites_list = sites_list.filter(Q(nom__icontains=query) | Q(client_nom__icontains=query))

    # Récupération des contrôles de la semaine
    controles_semaine = ControleSite.objects.filter(date__gte=debut_semaine)
    
    # Dictionnaire de comptage {site_id: nombre_de_visites}
    comptage = controles_semaine.values('site_id').annotate(total=Count('id'))
    visites_dict = {item['site_id']: item['total'] for item in comptage}

    # Construction de la donnée pour le template
    data_couverture = []
    for site in sites_list:
        nb_visites = visites_dict.get(site.id, 0)
        data_couverture.append({
            'site': site,
            'visites': nb_visites,
            'complet': nb_visites >= 2,
            'manquant': max(0, 2 - nb_visites)
        })

    # Pagination (25 sites par page pour gérer les 200 sites)
    paginator = Paginator(data_couverture, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'debut_semaine': debut_semaine,
        'query': query,
    }
    return render(request, 'users/direction/couverture.html', context)

@login_required
def resoudre_incident(request, controle_id):
    if request.user.role in ['admin', 'direction']:
        controle = get_object_or_404(ControleSite, id=controle_id)
        controle.incident_resolu = True
        controle.date_resolution = timezone.now()
        controle.save()
    return redirect('dashboard_admin')


@login_required
def admin_site_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        code = request.POST.get('code_site')
        client = request.POST.get('client_nom')
        adresse = request.POST.get('adresse')
        nb_prevus = request.POST.get('nb_prevus')
        
        # Création de l'objet Site
        nouveau_site = Site.objects.create(
            nom=nom,
            code_site=code,
            client_nom=client,
            adresse=adresse,
            nombre_techniciens_prevus=nb_prevus,
            actif=True
        )
        return redirect('admin_site_list')
        
    return render(request, 'users/direction/sites/admin_create.html')

from django.core.paginator import Paginator

@login_required
def admin_site_list(request):
    # Récupération de tous les sites
    sites_list = Site.objects.all().annotate(
        nb_tech_reels=Count('techniciens')
    ).order_by('nom')

    # Pagination : 20 sites par page
    paginator = Paginator(sites_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/direction/sites/admin_list.html', {'page_obj': page_obj})

@login_required
def admin_site_detail(request, pk):
    site = get_object_or_404(Site, pk=pk)
    techniciens = site.techniciens.all() # Utilise le related_name='techniciens'
    
    if request.method == 'POST':
        # Mise à jour rapide du nombre prévu et de l'état
        site.nombre_techniciens_prevus = request.POST.get('nb_prevus')
        site.actif = 'actif' in request.POST
        site.save()
        return redirect('admin_site_list')

    return render(request, 'users/direction/sites/admin_detail.html', {
        'site': site,
        'techniciens': techniciens,
        'techniciens_disponibles': Technicien.objects.exclude(site=site).filter(actif=True)
    })
 

@login_required
def affecter_technicien_existant(request, site_id):
    if request.method == "POST":
        technicien_id = request.POST.get('technicien_id')
        site = get_object_or_404(Site, id=site_id)
        technicien = get_object_or_404(Technicien, id=technicien_id)
        
        # Affectation au site
        technicien.site = site
        technicien.save()
        
    return redirect('admin_site_detail', pk=site_id)

@login_required
def retirer_technicien_site(request, tech_id):
    technicien = get_object_or_404(Technicien, id=tech_id)
    site_id = technicien.site.id if technicien.site else None
    
    # On retire l'affectation (devient intermittent / disponible)
    technicien.site = None
    technicien.save()
    
    if site_id:
        return redirect('admin_site_detail', pk=site_id)
    return redirect('admin_site_list')


@login_required
def liste_incidents_critiques(request):
    # Filtrage par statut via l'URL (ex: ?statut=resolu)
    statut = request.GET.get('statut', 'actifs')
    
    if statut == 'resolu':
        incidents_list = ControleSite.objects.filter(incident=True, incident_resolu=True)
    else:
        incidents_list = ControleSite.objects.filter(incident=True, incident_resolu=False)

    incidents_list = incidents_list.select_related('site', 'superviseur').order_by('-date')

    # Pagination (15 incidents par page)
    paginator = Paginator(incidents_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/direction/incidents/liste.html', {
        'page_obj': page_obj,
        'statut': statut
    })





@login_required
def admin_rapport_list(request):
    query = request.GET.get('q', '')
    # On récupère tous les rapports avec les relations pour la performance
    rapports = ControleSite.objects.select_related('site', 'superviseur').order_by('-date')

    if query:
        rapports = rapports.filter(
            Q(site__nom__icontains=query) | 
            Q(superviseur__last_name__icontains=query)
        )

    paginator = Paginator(rapports, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "users/direction/rapport/rapport_list.html", {
        "page_obj": page_obj,
        "query": query
    })

@login_required
def admin_rapport_detail(request, pk):
    rapport = get_object_or_404(ControleSite, pk=pk)
    return render(request, "users/direction/rapport/rapport_detail.html", {"rapport": rapport})

