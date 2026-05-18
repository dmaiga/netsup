from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialise tous les sites pour le superviseur Samake'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL(f"RENIATILISATION DE LA BASE DE DONNEES..."))

        self.stdout.write(self.style.MIGRATE_LABEL(f"Importation des sites de SAMAKE..."))
        # Récupération du superviseur spécifique
        superviseur = User.objects.filter(telephone="74034488").first()

        if not superviseur:
            self.stdout.write(self.style.ERROR("Superviseur Samake (74034488) introuvable. Lancez seed_users d'abord."))
            return

        # Liste exhaustive des sites de Samake
        sites_data = [
            {"nom": "PALAIS PRESIDENTIELLE", "lieu": "KOULOUBA", "eff": 11, "code": "SK-001"},
            {"nom": "CONTENTIEUX", "lieu": "DARSALAM", "eff": 6, "code": "SK-002"},
            {"nom": "OXFAM + GUEST", "lieu": "KOROFINA", "eff": 7, "code": "SK-003"},
            {"nom": "CABINET BAH DAO", "lieu": "SOTUBA", "eff": 4, "code": "SK-004"},
            {"nom": "DOMICILE BAH DAO", "lieu": "CITE DU NIGER", "eff": 3, "code": "SK-005"},
            {"nom": "DOMICILE IBK", "lieu": "SEBENIKORO", "eff": 6, "code": "SK-006"},
            {"nom": "BANQUE MONDIALE", "lieu": "ACI 2000", "eff": 12, "code": "SK-007"},
            {"nom": "REFONDATION", "lieu": "BAMAKO COURA", "eff": 5, "code": "SK-008"},
            {"nom": "YARA CITE", "lieu": "CITE DU NIGER", "eff": 4, "code": "SK-009"},
            {"nom": "YARA ACI", "lieu": "ACI 2000", "eff": 2, "code": "SK-010"},
            {"nom": "YARA GOLF", "lieu": "BACO DJICORONI GOLF", "eff": 2, "code": "SK-011"},
            {"nom": "CLINIQUE NOCTURE", "lieu": "ALL DE BAMAKO", "eff": 5, "code": "SK-012"},
            {"nom": "CENTRE D'ACCUEIL 1", "lieu": "BASE - B", "eff": 2, "code": "SK-013"},
            {"nom": "CENTRE D'ACCUEIL 2", "lieu": "BASE - B", "eff": 1, "code": "SK-014"},
            {"nom": "HCNLS", "lieu": "ACI 2000", "eff": 6, "code": "SK-015"},
            {"nom": "PSI MALI", "lieu": "ACI 2000", "eff": 2, "code": "SK-016"},
            {"nom": "CIRA MALI", "lieu": "ACI 2000", "eff": 8, "code": "SK-017"},
            {"nom": "IMMEUBLE BAMA", "lieu": "ACI 2000", "eff": 8, "code": "SK-018"},
            {"nom": "GROUPE COMES", "lieu": "ACI 2000", "eff": 7, "code": "SK-019"},
            {"nom": "AEROPORT", "lieu": "AEROPORT", "eff": 6, "code": "SK-020"},
            {"nom": "PATRONAT", "lieu": "ACI 2000", "eff": 9, "code": "SK-021"},
            {"nom": "TEYLIUM", "lieu": "ACI 2000", "eff": 7, "code": "SK-022"},
            {"nom": "CABINET MAITRE HAKO", "lieu": "ACI 2000", "eff": 3, "code": "SK-023"},
            {"nom": "CLINIQUE WASSA", "lieu": "DJICORONI PARA", "eff": 5, "code": "SK-024"},
            {"nom": "ASAM", "lieu": "ACI 2000", "eff": 1, "code": "SK-025"},
            {"nom": "YARA MAMADOU", "lieu": "ACI 2000", "eff": 8, "code": "SK-026"},
            {"nom": "CABINET MAITRE TRAORE", "lieu": "ACI 2000", "eff": 1, "code": "SK-027"},
            {"nom": "STATION PETRO BAMA", "lieu": "BANAKORO", "eff": 0, "code": "SK-028"},
            {"nom": "CECI MALI", "lieu": "ACI 2000", "eff": 5, "code": "SK-029"},
            {"nom": "GECI Expert Conseil", "lieu": "ACI 2000", "eff": 3, "code": "SK-030"},
            {"nom": "Immof", "lieu": "ACI 2000", "eff": 6, "code": "SK-031"},
            {"nom": "CIFA Bourse", "lieu": "ACI 2000", "eff": 2, "code": "SK-032"},
            {"nom": "DGCE", "eff": 5, "lieu":"-"},
            {"nom": "CESAG", "eff": 3, "lieu":"-"},
            {"nom": "BENKAN", "eff": 1, "lieu":"-"},
            {"nom": "HAUT CONSEIL", "eff": 8, "lieu":"-"},
            {"nom": "IMMOAF", "eff": 3, "lieu":"-"},
            {"nom": "IMMOAS", "eff": 1, "lieu":"-"},
            {"nom": "IMMDAF", "eff": 1, "lieu":"-"},
            {"nom": "SIRA MALI", "eff": 2, "lieu":"-"},
            {"nom": "NET SUP", "eff": 1, "lieu":"-"},
            {"nom": "BATCHILY ACI", "eff": 5, "lieu":"-"},
            {"nom": "IMMEUBLE BATCHILY", "eff": 3, "lieu":"-"},
            {"nom": "TELIUM", "eff": 7, "lieu":"-"},
            {"nom": "TELIUM CIRA", "eff": 2, "lieu":"-"},
            {"nom": "TELIUM MAIRIE CIV", "eff": 1, "lieu":"-"},
            {"nom": "SITE AEROPORT", "eff": 1, "lieu":"-"},
            {"nom": "APPARTEMENT YARA GOLF", "eff": 1, "lieu":"-"},
        ]

        count = 0
        for data in sites_data:
            site, created = Site.objects.update_or_create(
                nom=data["nom"],
                adresse=data["lieu"],
                defaults={
                    "nombre_techniciens_prevus": data["eff"],
                    "superviseur": superviseur,
                    "actif": True
                }
            )

            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f" Terminé : {count} nouveaux sites créés pour Samake sur 32."))