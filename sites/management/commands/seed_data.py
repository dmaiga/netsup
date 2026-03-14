from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site, Technicien
from controles.models import ControleSite  # Vérifie le nom de ton app
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seed NETSUP : 50 Sites avec agents rattachés et rapports fictifs"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO(" Construction du parc NETSUP..."))

        # 1. Nettoyage (Optionnel mais conseillé pour le dev)
        ControleSite.objects.all().delete()
        Technicien.objects.all().delete()
        Site.objects.all().delete()

        # 2. Superviseurs
        supervisors = []
        for i, name in enumerate(["Moussa", "Fanta", "Oumar", "Fatou"]):
            user, _ = User.objects.update_or_create(
                username=f"sup_{name.lower()}",
                defaults={"first_name": name, "last_name": "Pro", "role": "superviseur", "telephone": f"7010000{i}"}
            )
            user.set_password("pass123")
            user.save()
            supervisors.append(user)

        # 3. Sites & Agents (Le cœur du système)
        zones = ["Bamako Coura", "ACI 2000", "Badalabougou", "Hamdallaye", "Magnambougou"]
        clients = ["Orange", "BNDA", "EDM", "Canal+", "Vivo Energy", "TotalEnergies"]
        
        all_techs = []
        self.stdout.write(f" Génération de 50 sites...")

        for i in range(1, 51):
            nom_site = f"{random.choice(clients)} - {random.choice(zones)} #{i}"
            nb_prevu = random.randint(3, 15) # Entre 3 et 15 agents par site
            
            site = Site.objects.create(
                code_site=f"S{1000+i}",
                nom=nom_site,
                adresse=random.choice(zones),
                client_nom=nom_site.split(' - ')[0],
                nombre_techniciens_prevus=nb_prevu
            )
            site.generate_qr_code()
            site.save()

            # Création des agents pour CE site précisément
            for j in range(nb_prevu):
                all_techs.append(Technicien(
                    nom=f"NOM-{i}-{j}",
                    prenom=f"Agent",
                    telephone=f"600{i:02d}{j:02d}",
                    type_contrat=random.choice(['cdi', 'cdd']),
                    site=site,
                    actif=True
                ))

        Technicien.objects.bulk_create(all_techs)
        self.stdout.write(self.style.SUCCESS(f" {len(all_techs)} agents créés et répartis sur 50 sites."))

        # 4. Rapports de Contrôle (Pour peupler tes graphiques)
        self.stdout.write(" Génération des rapports de contrôle récents...")
        rapports = []
        for site in Site.objects.all()[:30]: # On fait des rapports pour 30 sites
            for d in range(3): # 3 rapports par site à des dates différentes
                date_rapport = datetime.now() - timedelta(days=d)
                prevus = site.nombre_techniciens_prevus
                presents = random.randint(prevus-2, prevus) # Parfois des absents
                
                rapports.append(ControleSite(
                    site=site,
                    superviseur=random.choice(supervisors),
                    date=date_rapport,
                    techniciens_prevus=prevus,
                    techniciens_presents=max(0, presents),
                    techniciens_absents=max(0, prevus - presents),
                    etat_proprete=random.choice(['tres_propre', 'propre', 'moyen', 'mauvais']),
                    incident=random.choice([True, False, False, False]), # 25% de chance d'incident
                    observations="Contrôle de routine effectué.",
                    gps_lat=12.6392,
                    gps_long=-8.0029
                ))
        
        ControleSite.objects.bulk_create(rapports)
        self.stdout.write(self.style.SUCCESS(f" {len(rapports)} rapports de contrôle générés."))