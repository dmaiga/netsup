from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialise uniquement les sites pour le superviseur Moussa CISSE'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("Création des sites pour CISSE..."))

        # 1. Récupération du superviseur
        superviseur = User.objects.filter(telephone="76471572").first()

        if not superviseur:
            self.stdout.write(self.style.ERROR(" Superviseur Cissé (76471572) introuvable. Lancez seed_users d'abord."))
            return

        # 2. Liste des sites et effectifs fournis
        sites_data = [
            {"nom": "Ubpharm", "eff": 10, "code": "CS-001"},
            {"nom": "Assurance Bleu", "eff": 10, "code": "CS-002"},
            {"nom": "ARCAD Direction", "eff": 8, "code": "CS-003"},
            {"nom": "SBN Direction", "eff": 8, "code": "CS-004"},
            {"nom": "CAMED", "eff": 5, "code": "CS-005"},
            {"nom": "Clinique Karahinbe", "eff": 4, "code": "CS-006"},
            {"nom": "Events", "eff": 3, "code": "CS-007"},
            {"nom": "Juris Partner", "eff": 3, "code": "CS-008"},
            {"nom": "ARCAD Serpent", "eff": 3, "code": "CS-009"},
            {"nom": "INPS", "eff": 3, "code": "CS-010"},
            {"nom": "HEP", "eff": 2, "code": "CS-011"},
            {"nom": "SEMICA", "eff": 2, "code": "CS-012"},
            {"nom": "SBN Faso kanu", "eff": 1, "code": "CS-013"},
            {"nom": "SBN ACI 2000", "eff": 1, "code": "CS-014"},
            {"nom": "SBN Bamakocoura", "eff": 1, "code": "CS-015"},
            {"nom": "ARCAD Observatoire", "eff": 1, "code": "CS-016"},
            {"nom": "CSAC", "eff": 1, "code": "CS-017"},
            {"nom": "Yara Cite", "eff": 1, "code": "CS-018"},
            {"nom": "Patronat", "eff": 1, "code": "CS-019"},
            {"nom": "Banque Mondiale", "eff": 1, "code": "CS-020"},
        ]

        count = 0
        for data in sites_data:
            site, created = Site.objects.update_or_create(
                nom=data["nom"],
                superviseur=superviseur,  
                defaults={
                    "adresse": "Lieu non défini",
                    "nombre_techniciens_prevus": data["eff"],
                    "actif": True
                }
            )
        
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f" Terminé : {count} nouveaux sites créés pour Cissé sur 20."))