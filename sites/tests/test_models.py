from django.test import TestCase

from users.models import User, Technicien

from sites.models import Site, AffectationAgent


class SiteModelTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="superviseur_site",
            telephone="71000001",
            role="superviseur"
        )

    def test_generate_code_site(self):

        site = Site.objects.create(
            nom="Site Cissé",
            adresse="Bamako",
            client_nom="Client Test",
            nombre_techniciens_prevus=5,
            superviseur=self.superviseur
        )

        self.assertTrue(site.code_site.startswith("site_cisse"))

    def test_generate_unique_code_site(self):

        site1 = Site.objects.create(
            nom="Site Test",
            adresse="Adresse 1",
            client_nom="Client",
            nombre_techniciens_prevus=2,
            superviseur=self.superviseur
        )

        site2 = Site.objects.create(
            nom="Site Test",
            adresse="Adresse 2",
            client_nom="Client",
            nombre_techniciens_prevus=3,
            superviseur=self.superviseur
        )

        self.assertNotEqual(
            site1.code_site,
            site2.code_site
        )

    def test_qr_code_generated(self):

        site = Site.objects.create(
            nom="Site QR",
            adresse="Bamako",
            client_nom="Client QR",
            nombre_techniciens_prevus=4,
            superviseur=self.superviseur
        )

        self.assertTrue(site.qr_code)

    def test_site_str(self):

        site = Site.objects.create(
            nom="Site String",
            adresse="Bamako",
            client_nom="Client",
            nombre_techniciens_prevus=1,
            superviseur=self.superviseur
        )

        self.assertEqual(
            str(site),
            "Site String"
        )


class AffectationAgentTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super_affect",
            telephone="71000002",
            role="superviseur"
        )

        self.technicien = Technicien.objects.create(
            nom="Diallo",
            prenom="Moussa",
            telephone="71000003",
            genre="M",
            superviseur=self.superviseur
        )

        self.site = Site.objects.create(
            nom="Site Affectation",
            adresse="Bamako",
            client_nom="Client",
            nombre_techniciens_prevus=3,
            superviseur=self.superviseur
        )

    def test_affectation_creation(self):

        affectation = AffectationAgent.objects.create(
            technicien=self.technicien,
            site=self.site
        )

        self.assertEqual(
            affectation.technicien,
            self.technicien
        )

        self.assertEqual(
            affectation.site,
            self.site
        )

        self.assertTrue(affectation.actif)

    def test_get_agents_actifs(self):

        AffectationAgent.objects.create(
            technicien=self.technicien,
            site=self.site,
            actif=True
        )

        agents = self.site.get_agents_actifs()

        self.assertIn(
            self.technicien,
            agents
        )