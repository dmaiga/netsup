# users/views_superviseur.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from sites.models import Site, AffectationAgent


from django.utils import timezone

from users.forms import TechnicienTerrainForm


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
            'dashboard_superviseur'
        )

    context = {
        'form': form
    }

    return render(
        request,
        'users/superviseur/create_technicien.html',
        context
    )

