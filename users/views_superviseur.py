# users/views_superviseur.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from sites.models import Site, AffectationAgent


from django.utils import timezone

from users.forms import TechnicienTerrainForm
from users.models import Technicien


@login_required
def create_technicien(request):

    form = TechnicienTerrainForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        technicien = form.save(commit=False)

        technicien.superviseur = request.user

        technicien.save()

        return redirect(
            'technicien_list'
        )

    context = {
        'form': form
    }

    return render(
        request,
        'users/superviseur/create_technicien.html',
        context
    )


@login_required
def technicien_list(request):

    techniciens = (
        Technicien.objects
        .filter(
            superviseur=request.user
        )
        .order_by('prenom', 'nom')
    )

    context = {
        'techniciens': techniciens
    }

    return render(
        request,
        'users/superviseur/technicien_list.html',
        context
    )


@login_required
def technicien_detail(request, pk):

    technicien = get_object_or_404(
        Technicien,
        pk=pk,
        superviseur=request.user
    )

    sites = technicien.get_sites_actifs()

    context = {
        'technicien': technicien,
        'sites': sites
    }

    return render(
        request,
        'users/superviseur/technicien_detail.html',
        context
    )