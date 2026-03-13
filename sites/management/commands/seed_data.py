from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sites.models import Site, Technicien

import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with demo data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Creating supervisors...")

        supervisors = []

        for i in range(2):

            user, created = User.objects.get_or_create(
                username=f"superviseur{i}",
                defaults={
                    "role": "superviseur",
                    "telephone": f"7000000{i}",
                }
            )

            if created:
                user.set_password("pass123")
                user.save()

            supervisors.append(user)

        self.stdout.write("Supervisors ready")


        self.stdout.write("Creating sites...")

        sites = []

        for i in range(20):

            site, created = Site.objects.get_or_create(
                code_site=f"SITE{i+1}",
                defaults={
                    "nom": f"Site {i+1}",
                    "adresse": "Bamako",
                    "client_nom": f"Client {i+1}",
                    "nombre_techniciens_prevus": random.randint(5, 15),
                }
            )

            # Générer QR code si absent
            if not site.qr_code:
                site.generate_qr_code()
                site.save(update_fields=["qr_code"])

            sites.append(site)

        self.stdout.write("Sites ready")


        self.stdout.write("Creating technicians...")

        for i in range(200):

            site = random.choice(sites)

            Technicien.objects.create(
                nom=f"Technicien{i}",
                prenom="NETSUP",
                telephone=f"+22376000{i}",
                type_contrat="cdi",
                site=site
            )

        self.stdout.write("Technicians created")

        self.stdout.write(self.style.SUCCESS("Seeding complete"))