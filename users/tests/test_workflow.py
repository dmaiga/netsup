from django.test import TestCase

from users.models import User, Technicien

from sites.models import (
    Site,
    AffectationAgent
)

from controles.models import (
    ControleSite,
    PointageAgent
)


class WorkflowIntegrationTest(TestCase):

    def test_complete_terrain_workflow(self):

        # 1. Superviseur
        superviseur = User.objects.create(
            username="superviseur_workflow",
            telephone="73000001",
            role="superviseur"
        )

        # 2. Technicien
        technicien = Technicien.objects.create(
            nom="Diallo",
            prenom="Moussa",
            telephone="73000002",
            genre="M",
            superviseur=superviseur
        )

        # 3. Site
        site = Site.objects.create(
            nom="Site Workflow",
            adresse="Bamako",
            client_nom="Client Workflow",
            nombre_techniciens_prevus=1,
            superviseur=superviseur
        )

        # 4. Affectation
        affectation = AffectationAgent.objects.create(
            technicien=technicien,
            site=site,
            actif=True
        )

        self.assertEqual(
            site.get_agents_actifs().count(),
            1
        )

        # 5. Contrôle
        controle = ControleSite.objects.create(
            site=site,
            superviseur=superviseur,
            techniciens_prevus=1,
            techniciens_presents=1,
            techniciens_absents=0,
            etat_proprete="propre",
            incident=False
        )

        # 6. Pointage
        pointage = PointageAgent.objects.create(
            controle=controle,
            technicien=technicien,
            present=True
        )

        # 7. Vérifications métier

        self.assertEqual(
            controle.taux_presence,
            100
        )

        self.assertTrue(
            pointage.present
        )

        self.assertEqual(
            controle.pointages.count(),
            1
        )

        self.assertEqual(
            str(technicien),
            "Moussa Diallo"
        )