from django.test import TestCase

from users.models import User

from sites.forms import (
    SiteForm,
    SuperviseurSiteForm
)


class SiteFormTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super_form",
            telephone="71000004",
            role="superviseur"
        )

    def test_site_form_valid(self):

        form = SiteForm(data={
            "nom": "Site Test",
            "adresse": "Bamako",
            "client_nom": "Client Test",
            "nombre_techniciens_prevus": 5,
            "latitude": 12.6392,
            "longitude": -8.0029,
            "superviseur": self.superviseur.id,
            "actif": True
        })

        self.assertTrue(form.is_valid())

    def test_site_form_invalid_without_nom(self):

        form = SiteForm(data={
            "adresse": "Bamako",
            "client_nom": "Client Test",
            "nombre_techniciens_prevus": 5
        })

        self.assertFalse(form.is_valid())

        self.assertIn(
            "nom",
            form.errors
        )


class SuperviseurSiteFormTest(TestCase):

    def test_superviseur_site_form_valid(self):

        form = SuperviseurSiteForm(data={
            "nom": "Site Superviseur",
            "adresse": "Bamako",
            "client_nom": "Client",
            "nombre_techniciens_prevus": 2,
            "latitude": 12.6,
            "longitude": -8.0
        })

        self.assertTrue(form.is_valid())