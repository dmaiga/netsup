# sites/views_superviseur.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SuperviseurSiteForm
from django.shortcuts import get_object_or_404

from .models import Site
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from django.shortcuts import get_object_or_404

from sites.models import Site, AffectationAgent




@login_required
def create_site(request):

    form = SuperviseurSiteForm(
        request.POST or None
    )

    if form.is_valid():

        site = form.save(commit=False)

        site.superviseur = request.user

        site.save()

        return redirect(
            'site_detail',
            site_id=site.id
        )

    context = {
        'form': form
    }

    return render(
        request,
        'sites/superviseur/create_site.html',
        context
    )

# sites/views_superviseur.py

@login_required
def liste_site(request):

    sites = Site.objects.filter(
        superviseur=request.user
    ).prefetch_related(
        'affectations'
    )

    context = {
        'sites': sites
    }

    return render(
        request,
        'sites/superviseur/liste_site.html',
        context
    )

@login_required
def site_detail(request, site_id):

    site = get_object_or_404(
        Site,
        id=site_id,
        superviseur=request.user
    )

    techniciens = site.get_agents_actifs()

    context = {
        'site': site,
        'techniciens': techniciens
    }

    return render(
        request,
        'sites/superviseur/site_detail.html',
        context
    )


from users.forms import AffectationTechnicienForm


@login_required
def affecter_technicien(request, site_id):

    site = get_object_or_404(
        Site,
        id=site_id,
        superviseur=request.user
    )

    form = AffectationTechnicienForm(
        request.POST or None,
        superviseur=request.user
    )

    if form.is_valid():

        technicien = form.cleaned_data['technicien']

        already_exists = AffectationAgent.objects.filter(
            technicien=technicien,
            site=site,
            actif=True
        ).exists()

        if not already_exists:

            AffectationAgent.objects.create(
                technicien=technicien,
                site=site
            )

        return redirect(
            'site_detail',
            site_id=site.id
        )

    context = {
        'site': site,
        'form': form
    }

    return render(
        request,
        'sites/superviseur/affecter_technicien.html',
        context
    )




@login_required
def retirer_technicien(request, affectation_id):

    affectation = get_object_or_404(
        AffectationAgent,
        id=affectation_id,
        site__superviseur=request.user
    )

    affectation.actif = False
    affectation.date_fin = timezone.now().date()

    affectation.save()

    return redirect(
        'site_detail',
        site_id=affectation.site.id
    )