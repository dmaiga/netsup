from django.test import TestCase

from users.models import User, Technicien

from sites.models import Site

from controles.models import (
    ControleSite,
    PointageAgent
)


class ControleSiteModelTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="superviseur_controle",
            telephone="72000001",
            role="superviseur"
        )

        self.site = Site.objects.create(
            nom="Site Contrôle",
            adresse="Bamako",
            client_nom="Client Contrôle",
            nombre_techniciens_prevus=5,
            superviseur=self.superviseur
        )

    def test_controle_creation(self):

        controle = ControleSite.objects.create(
            site=self.site,
            superviseur=self.superviseur,
            techniciens_prevus=5,
            techniciens_presents=4,
            techniciens_absents=1,
            etat_proprete="propre"
        )

        self.assertEqual(
            controle.site,
            self.site
        )

        self.assertEqual(
            controle.superviseur,
            self.superviseur
        )

    def test_taux_presence(self):

        controle = ControleSite.objects.create(
            site=self.site,
            superviseur=self.superviseur,
            techniciens_prevus=10,
            techniciens_presents=8,
            techniciens_absents=2,
            etat_proprete="propre"
        )

        self.assertEqual(
            controle.taux_presence,
            80
        )

    def test_taux_presence_zero(self):

        controle = ControleSite.objects.create(
            site=self.site,
            superviseur=self.superviseur,
            techniciens_prevus=0,
            techniciens_presents=0,
            techniciens_absents=0,
            etat_proprete="moyen"
        )

        self.assertEqual(
            controle.taux_presence,
            0
        )


class PointageAgentModelTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super_pointage",
            telephone="72000002",
            role="superviseur"
        )

        self.site = Site.objects.create(
            nom="Site Pointage",
            adresse="Bamako",
            client_nom="Client",
            nombre_techniciens_prevus=2,
            superviseur=self.superviseur
        )

        self.technicien = Technicien.objects.create(
            nom="Diallo",
            prenom="Moussa",
            telephone="72000003",
            genre="M",
            superviseur=self.superviseur
        )

        self.controle = ControleSite.objects.create(
            site=self.site,
            superviseur=self.superviseur,
            techniciens_prevus=2,
            techniciens_presents=1,
            techniciens_absents=1,
            etat_proprete="propre"
        )

    def test_pointage_present(self):

        pointage = PointageAgent.objects.create(
            controle=self.controle,
            technicien=self.technicien,
            present=True
        )

        self.assertTrue(pointage.present)

    def test_pointage_str_present(self):

        pointage = PointageAgent.objects.create(
            controle=self.controle,
            technicien=self.technicien,
            present=True
        )

        self.assertIn(
            "présent",
            str(pointage)
        )

    def test_pointage_str_absent(self):

        pointage = PointageAgent.objects.create(
            controle=self.controle,
            technicien=self.technicien,
            present=False,
            motif_absence="maladie"
        )

        self.assertIn(
            "absent",
            str(pointage)
        )