from django.test import TestCase

from users.models import User, Technicien

from sites.models import Site

from controles.forms import (
    ControleSiteForm,
    build_pointage_formset
)


class ControleSiteFormTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super_form_controle",
            telephone="72000004",
            role="superviseur"
        )

        self.site = Site.objects.create(
            nom="Site Form",
            adresse="Bamako",
            client_nom="Client",
            nombre_techniciens_prevus=3,
            superviseur=self.superviseur
        )

    def test_form_valid_without_incident(self):

        form = ControleSiteForm(
            data={
                "etat_proprete": "propre",
                "incident": False,
                "problemes": "",
                "observations": "RAS"
            },
            site=self.site
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_incident_without_problem(self):

        form = ControleSiteForm(
            data={
                "etat_proprete": "mauvais",
                "incident": True,
                "problemes": "",
                "observations": "Incident détecté"
            },
            site=self.site
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "problemes",
            form.errors
        )

    def test_form_valid_with_incident_and_problem(self):

        form = ControleSiteForm(
            data={
                "etat_proprete": "mauvais",
                "incident": True,
                "problemes": "Panne électrique",
                "observations": "Urgent"
            },
            site=self.site
        )

        self.assertTrue(form.is_valid())


class PointageFormsetTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super_formset",
            telephone="72000005",
            role="superviseur"
        )

        self.tech1 = Technicien.objects.create(
            nom="Diallo",
            prenom="Moussa",
            telephone="72000006",
            genre="M",
            superviseur=self.superviseur
        )

        self.tech2 = Technicien.objects.create(
            nom="Traore",
            prenom="Awa",
            telephone="72000007",
            genre="F",
            superviseur=self.superviseur
        )

    def test_build_pointage_formset(self):

        agents = [self.tech1, self.tech2]

        formset = build_pointage_formset(agents)

        self.assertEqual(
            len(formset.forms),
            2
        )

        self.assertEqual(
            formset.forms[0].initial["nom_affiche"],
            "Moussa Diallo"
        )

        self.assertTrue(
            formset.forms[0].initial["present"]
        )