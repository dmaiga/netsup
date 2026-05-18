from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 

from sites.models import Site,AffectationAgent
from controles.models import ControleSite

from users.models import User,Technicien
from users.forms import UserForm

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
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain


from controles.models import PointageAgent
from django.db.models import Avg, FloatField, ExpressionWrapper, F
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Count
from django.db.models import Q
from django.utils import timezone
from datetime import datetime


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

    total_sites = Site.objects.filter(actif=True,superviseur=request.user).count()

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



@login_required
def user_list(request):
    query = request.GET.get('q', '')
    
    # 1. Superviseurs
    users_qs = User.objects.filter(is_deleted=False, is_superuser=False).order_by('last_name')
    
    # 2. Techniciens avec comptage des sites actifs
    # On filtre le Count pour ne prendre que les affectations marquées comme 'actives'
    techs_qs = Technicien.objects.filter(actif=True).annotate(
        nb_sites=Count('affectations', filter=Q(affectations__actif=True))
    ).order_by('nom')

    if query:
        users_qs = users_qs.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        techs_qs = techs_qs.filter(Q(nom__icontains=query) | Q(prenom__icontains=query))

    # Pagination
    paginator_techs = Paginator(techs_qs, 10) 
    page_techs = request.GET.get('page_techs')
    techs_obj = paginator_techs.get_page(page_techs)

    return render(request, "users/user/list.html", {
        "users": users_qs,
        "techs": techs_obj,
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
    ).select_related('site', 'superviseur').order_by('-date')[:10]

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
    return render(request, "users/dashboard/administration.html", context)


@login_required
def couverture_hebdo(request):
    date_str = request.GET.get('date')
    aujourd_hui = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    fin_semaine = debut_semaine + timedelta(days=6)
    
    # 2. Récupération des filtres
    query = request.GET.get('q', '')
    sup_id = request.GET.get('superviseur')

    # 3. Filtrage des sites
    sites_list = Site.objects.filter(actif=True).order_by('nom')

    if query:
        sites_list = sites_list.filter(Q(nom__icontains=query) | Q(client_nom__icontains=query))

    
    if sup_id and sup_id != "None" and sup_id.strip() != "":
        sites_list = sites_list.filter(superviseur_id=sup_id)
    # 4. Calcul de la performance (KPI)
    controles_semaine = ControleSite.objects.filter(
        date__date__gte=debut_semaine,
        date__date__lte=fin_semaine
    )
    
    # Dictionnaire des visites par site
    comptage = controles_semaine.values('site_id').annotate(total=Count('id'))
    visites_dict = {item['site_id']: item['total'] for item in comptage}

    data_couverture = []
    total_visites_effectuees = 0
    for site in sites_list:
        nb_visites = visites_dict.get(site.id, 0)
        total_visites_effectuees += nb_visites
        data_couverture.append({
            'site': site,
            'visites': nb_visites,
            'complet': nb_visites >= 2,
            'manquant': max(0, 2 - nb_visites)
        })

    # Calcul KPI pour le bandeau supérieur
    objectif_total = sites_list.count() * 2
    performance_globale = (total_visites_effectuees / objectif_total * 100) if objectif_total > 0 else 0

    # Pagination
    paginator = Paginator(data_couverture, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Pour le filtre select
    tous_superviseurs = User.objects.filter(role='superviseur', is_active=True)

    context = {
        'page_obj': page_obj,
        'debut_semaine': debut_semaine,
        'fin_semaine': fin_semaine,
        'query': query,
        'sup_id': sup_id,
        'tous_superviseurs': tous_superviseurs,
        'stats': {
            'objectif': objectif_total,
            'realise': total_visites_effectuees,
            'percent': round(performance_globale, 1),
            'nb_sites': sites_list.count()
        },
        'sup_id': sup_id if sup_id and sup_id != "None" else "",
        'semaine_precedente': (debut_semaine - timedelta(days=7)).strftime('%Y-%m-%d'),
        'semaine_suivante': (debut_semaine + timedelta(days=7)).strftime('%Y-%m-%d'),
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
    # Récupération des paramètres de filtrage
    query = request.GET.get('q', '')
    site_id = request.GET.get('site', '')
    superviseur_id = request.GET.get('superviseur', '')
    etat = request.GET.get('etat', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')

    # Base Queryset
    rapports = ControleSite.objects.select_related(
        'site', 
        'site__superviseur',
        'superviseur'
        ).annotate(
                nb_affectes_actuels=Count(
                    'site__affectations', 
                    filter=Q(site__affectations__actif=True)
                )
        )
    
    # Recherche textuelle (Site ou Nom du superviseur)

    if query:
        rapports = rapports.filter(
            Q(site__nom__icontains=query) | 
            Q(superviseur__last_name__icontains=query) |
            Q(superviseur__username__icontains=query) |
            # Recherche par nom d'un technicien affecté au site du rapport
            Q(site__affectations__technicien__nom__icontains=query) |
            Q(site__affectations__technicien__prenom__icontains=query)
        ).distinct() # Important avec les filtres sur relations M2M

    # Filtre par Site spécifique
    if site_id:
        rapports = rapports.filter(site_id=site_id)

    # Filtre par Superviseur
    if superviseur_id:
        rapports = rapports.filter(superviseur_id=superviseur_id)

    # Filtre par État de propreté
    if etat:
        rapports = rapports.filter(etat_proprete=etat)

    # Filtres Temporels
    if date_debut:
        rapports = rapports.filter(date__date__gte=date_debut)
    if date_fin:
        rapports = rapports.filter(date__date__lte=date_fin)

    # Données pour les menus déroulants des filtres
    sites = Site.objects.all().order_by('nom')
    superviseurs = User.objects.filter(role='superviseur').order_by('username')
    etats = ControleSite.ETAT_CHOICES

        # Pagination
    paginator = Paginator(rapports, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        "page_obj": page_obj,
        "query": query,
        "sites": sites,
        "superviseurs": superviseurs,
        "etats": etats,
        # On renvoie les valeurs actuelles pour garder les filtres sélectionnés dans le HTML
        "selected_site": site_id,
        "selected_superviseur": superviseur_id,
        "selected_etat": etat,
        "date_debut": date_debut,
        "date_fin": date_fin,
    }

    return render(request, "users/direction/rapport/rapport_list.html", context)

@login_required
def admin_rapport_detail(request, pk):
    rapport = get_object_or_404(ControleSite.objects.select_related('site', 'superviseur'), pk=pk)
    
    # Récupérer les techniciens qui sont officiellement affectés à ce site
    # via le modèle AffectationAgent
    techniciens_affectes = Technicien.objects.filter(
        affectations__site=rapport.site,
        affectations__actif=True
    ).distinct()

    context = {
        "rapport": rapport,
        "techniciens_affectes": techniciens_affectes,
    }
    return render(request, "users/direction/rapport/rapport_detail.html", context)
# ─────────────────────────────────────────────
#  GESTION DES AFFECTATIONS (Direction)
# ─────────────────────────────────────────────


@login_required
def rapport_presence(request):
    """
    Rapport présence avec navigation temporelle (semaine / mois)
    """

    from django.db.models import Count, Sum, Case, When, IntegerField
    from datetime import datetime, timedelta
    import calendar

    # 🔹 paramètres
    type_periode = request.GET.get('type', 'semaine')  # semaine | mois
    date_str = request.GET.get('date')

    # 🔹 date courante
    if date_str:
        try:
            current_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            current_date = timezone.now()
    else:
        current_date = timezone.now()

    # 🔹 calcul période
    if type_periode == "mois":
        start = current_date.replace(day=1)
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        end = current_date.replace(day=last_day)

        prev_date = (start - timedelta(days=1)).replace(day=1)
        next_date = (end + timedelta(days=1)).replace(day=1)

    else:  # semaine par défaut
        start = current_date - timedelta(days=current_date.weekday())
        end = start + timedelta(days=6)

        prev_date = start - timedelta(days=7)
        next_date = start + timedelta(days=7)

    # 🔹 queryset filtré
    pointages_qs = PointageAgent.objects.filter(
        controle__date__date__range=[start, end]
    )

    # 🔹 stats agents
    stats_agents = pointages_qs.values(
        'technicien__id',
        'technicien__nom',
        'technicien__prenom',
    ).annotate(
        total=Count('id'),
        presents=Sum(Case(When(present=True, then=1), default=0, output_field=IntegerField())),
        absents=Sum(Case(When(present=False, then=1), default=0, output_field=IntegerField())),
    ).order_by('technicien__nom','-absents')

    # 🔥 enrichissement (sites + superviseur)
    from users.models import Technicien

    stats_agents = list(stats_agents)
    tech_ids = [row['technicien__id'] for row in stats_agents]
    from users.models import Technicien
    
    techniciens = Technicien.objects.filter(id__in=tech_ids).prefetch_related(
        'affectations__site__superviseur'
    )
    tech_map = {t.id: t for t in techniciens}
    for row in stats_agents:
        tech = tech_map.get(row['technicien__id'])

        if not tech:
            continue

        sites = [a.site for a in tech.affectations.filter(actif=True)]
        row['sites'] = sites

        row['superviseur'] = sites[0].superviseur if sites else None

        # taux
        if row['total'] and row['total'] > 0:
            row['taux'] = round((row['presents'] / row['total']) * 100)
        else:
            row['taux'] = None

    # 🔹 agents à risque
    agents_risque = [
        r for r in stats_agents
        if r['taux'] is not None and r['taux'] < 70 and r['total'] >= 3
    ]

    # 🔹 stats sites
    stats_sites = pointages_qs.values(
        'controle__site__id',
        'controle__site__nom',
    ).annotate(
        total=Count('id'),
        presents=Sum(Case(When(present=True, then=1), default=0, output_field=IntegerField())),
        absents=Sum(Case(When(present=False, then=1), default=0, output_field=IntegerField())),
    ).order_by('-absents')

    stats_sites = list(stats_sites)

    for row in stats_sites:
        if row['total'] and row['total'] > 0:
            row['taux'] = round((row['presents'] / row['total']) * 100)
        else:
            row['taux'] = None

    # 🔹 pagination agents
    paginator_agents = Paginator(stats_agents, 20)
    page_agents = paginator_agents.get_page(request.GET.get('page_agents'))

    # 🔹 render
    return render(request, 'users/direction/rapport/rapport_presence.html', {
        'stats_agents': page_agents,
        'stats_sites': stats_sites[:10],
        'agents_risque': agents_risque,

        # 🔥 période
        'type_periode': type_periode,
        'start': start,
        'end': end,
        'prev_date': prev_date,
        'next_date': next_date,
    })