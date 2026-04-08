from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site, AffectationAgent
from users.models import ProfilRH, Technicien, Conge
from controles.models import ControleSite, PointageAgent
import random
from datetime import timedelta, date
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = "Seed NETSUP : Gestion stricte des congés (CDI/CDD uniquement)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_LABEL("Nettoyage et réinitialisation..."))

        # Nettoyage des tables
        Conge.objects.all().delete()
        PointageAgent.objects.all().delete()
        ControleSite.objects.all().delete()
        AffectationAgent.objects.all().delete()
        ProfilRH.objects.all().delete()
        Technicien.objects.all().delete()
        Site.objects.all().delete()
        User.objects.filter(role__in=['direction','superviseur']).delete()

        # 🔹 1. CRÉATION DES SITES
        zones = ["ACI 2000", "Badalabougou", "Hamdallaye", "Magnambougou", "Sébénikoro"]
        clients = ["Orange", "BNDA", "EDM SA", "Canal+", "Vivo Energy"]
        sites_crees = [
            Site.objects.create(
                code_site=f"S-{100+i}",
                nom=f"{random.choice(clients)} - {random.choice(zones)}",
                adresse=random.choice(zones),
                client_nom=random.choice(clients),
                nombre_techniciens_prevus=random.randint(4, 6)
            ) for i in range(8)
        ]

        # 🔹 2. TECHNICIENS & PROFILS RH
        prenoms = ["Adama", "Bakary", "Chaka", "Djeneba", "Ibrahim", "Mariam", "Salif", "Oumou"]
        noms = ["Tounkara", "Coulibaly", "Koné", "Dembélé", "Maïga", "Traoré"]
        tech_pool = []

        for i in range(40):
            genre = random.choice(['M', 'F'])
            tech = Technicien.objects.create(
                matricule=f"T-2026-{i:03d}",
                nom=random.choice(noms),
                prenom=random.choice(prenoms),
                genre=genre,
                telephone=f"70000{i:03d}", # Unicité garantie
                quartier=random.choice(zones),
                actif=True
            )

            # Type de contrat aléatoire
            type_ct = random.choice(['cdi', 'cdd', 'prestation'])
            
            # Génération INPS/AMO (8-12 chiffres)
            # On ne met l'INPS/AMO que pour les salariés (CDI/CDD) par réalisme
            has_social_security = type_ct in ['cdi', 'cdd']
            inps = "".join([str(random.randint(0, 9)) for _ in range(10)]) if has_social_security else ""
            amo = f"{'1' if genre == 'M' else '2'}{random.randint(10000000, 99999999)}" if has_social_security else ""

            ProfilRH.objects.create(
                technicien=tech,
                type_contrat=type_ct,
                numero_inps=inps,
                numero_amo=amo,
                salaire=random.choice([80000, 100000, 120000, 150000]),
                type_horaire='temps_plein' if type_ct != 'prestation' else 'mi_temps',
                disponibilite=random.choice(['matin', 'soir', 'les_deux']),
                date_embauche=date(2025, random.randint(1, 12), random.randint(1, 28))
            )

            # 🔹 3. RÈGLE MÉTIER : CONGÉS (UNIQUEMENT CDI / CDD)
            if type_ct in ['cdi', 'cdd'] and random.random() < 0.25:
                debut = date.today() + timedelta(days=random.randint(-5, 10))
                Conge.objects.create(
                    technicien=tech,
                    date_debut=debut,
                    date_fin=debut + timedelta(days=random.randint(2, 7)),
                    motif=random.choice(["Permission", "Congé annuel", "Repos médical"]),
                    valide=True
                )
            
            tech_pool.append(tech)

        # 🔹 4. AFFECTATIONS & SUPERVISEURS (Identique au précédent)
        for site in sites_crees:
            agents = random.sample(tech_pool, site.nombre_techniciens_prevus)
            for a in agents:
                AffectationAgent.objects.create(technicien=a, site=site, actif=True)

        supervisors = []
        for name in ["Moussa", "Fanta"]:
            user = User.objects.create(
                username=name.lower(), first_name=name, role="superviseur",
                telephone=f"6611100{len(supervisors)}", is_active=True
            )
            user.set_password("pass123")
            user.save()
            supervisors.append(user)

        self.stdout.write(self.style.SUCCESS("Seed terminé : Congés appliqués uniquement aux contractuels."))