from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site
from users.models import Technicien
from controles.models import ControleSite, PointageAgent
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Simule 7 jours d'activité intense de contrôle sur les sites"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_LABEL("Début de la simulation d'activité..."))

        # 1. Récupération des acteurs
        superviseurs = list(User.objects.filter(role='superviseur'))
        sites = list(Site.objects.filter(actif=True))

        if not superviseurs or not sites:
            self.stdout.write(self.style.ERROR("Erreur : Créez d'abord des superviseurs et des sites."))
            return

        # Nettoyage des anciens contrôles pour repartir sur une semaine propre
        PointageAgent.objects.all().delete()
        ControleSite.objects.all().delete()

        # 2. Simulation sur les 7 derniers jours
        for day in range(7):
            date_du_jour = timezone.now() - timedelta(days=day)
            self.stdout.write(f"Simulation du jour : {date_du_jour.date()}")

            for site in sites:
                # On récupère les agents réellement affectés à ce site
                agents_du_site = list(site.get_agents_actifs())
                
                if not agents_du_site:
                    continue

                # Un superviseur passe 1 à 2 fois par jour par site
                for passage in range(random.randint(1, 2)):
                    # Heure du passage (ex: entre 8h et 11h, ou 14h et 17h)
                    heure_base = 8 if passage == 0 else 14
                    moment_controle = date_du_jour.replace(
                        hour=heure_base + random.randint(0, 3),
                        minute=random.randint(0, 59)
                    )

                    # --- LOGIQUE DE PRÉSENCE ---
                    presents = []
                    absents = []
                    for agent in agents_du_site:
                        # 90% de chance d'être présent, sauf si c'est un dimanche (moins d'effectif)
                        seuil_presence = 0.1 if moment_controle.weekday() < 5 else 0.4
                        if random.random() > seuil_presence:
                            presents.append(agent)
                        else:
                            absents.append(agent)

                    # --- ÉTAT DU SITE & INCIDENTS ---
                    # Un site avec beaucoup d'absents a plus de chances d'être "Moyen" ou "Mauvais"
                    if len(absents) > 2:
                        etat = random.choice(['moyen', 'mauvais'])
                        incident = True
                        problemes = "Manque d'effectif critique, zones non traitées."
                    else:
                        etat = random.choice(['tres_propre', 'propre', 'moyen'])
                        incident = random.random() < 0.1 # 10% de chance d'incident technique
                        problemes = "Fuite d'eau signalée" if incident else ""

                    # 3. Création du rapport de contrôle
                    rapport = ControleSite.objects.create(
                        site=site,
                        superviseur=random.choice(superviseurs),
                        techniciens_prevus=len(agents_du_site),
                        techniciens_presents=len(presents),
                        techniciens_absents=len(absents),
                        etat_proprete=etat,
                        incident=incident,
                        problemes=problemes,
                        observations=f"Passage n°{passage+1}. RAS sur l'ensemble du site." if not incident else "Attention requise.",
                        gps_lat=12.6 + random.uniform(-0.05, 0.05),
                        gps_long=-8.0 + random.uniform(-0.05, 0.05)
                    )

                    # On force la date (car auto_now_add=True bloque la modif au .create)
                    ControleSite.objects.filter(id=rapport.id).update(date=moment_controle)

                    # 4. Pointages nominaux des agents de surface
                    for agent in presents:
                        PointageAgent.objects.create(
                            controle=rapport,
                            technicien=agent,
                            present=True
                        )

                    for agent in absents:
                        # Si l'agent est absent, on lui donne un motif
                        motif = random.choice(['retard', 'absent_np', 'maladie'])
                        PointageAgent.objects.create(
                            controle=rapport,
                            technicien=agent,
                            present=False,
                            motif_absence=motif
                        )

        self.stdout.write(self.style.SUCCESS(f"Simulation terminée : {ControleSite.objects.count()} rapports générés."))