from django.test import TestCase

from users.forms import (
    UserForm,
    TechnicienTerrainForm,
    AffectationTechnicienForm
)

from users.models import User, Technicien


class UserFormTest(TestCase):

    def test_user_form_valid(self):

        form = UserForm(data={
            "username": "admin1",
            "telephone": "70000011",
            "role": "admin",
            "password": "password123"
        })

        self.assertTrue(form.is_valid())

    def test_user_form_missing_username(self):

        form = UserForm(data={
            "telephone": "70000012",
            "role": "admin"
        })

        self.assertFalse(form.is_valid())

        self.assertIn(
            "username",
            form.errors
        )


class TechnicienTerrainFormTest(TestCase):

    def test_technicien_form_valid(self):

        form = TechnicienTerrainForm(data={
            "nom": "Diallo",
            "prenom": "Moussa",
            "telephone": "70000013",
            "genre": "M"
        })

        self.assertTrue(form.is_valid())

    def test_technicien_form_invalid_without_nom(self):

        form = TechnicienTerrainForm(data={
            "prenom": "Moussa",
            "telephone": "70000014",
            "genre": "M"
        })

        self.assertFalse(form.is_valid())

        self.assertIn(
            "nom",
            form.errors
        )


class AffectationTechnicienFormTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="super1",
            telephone="70000015",
            role="superviseur"
        )

        self.other_superviseur = User.objects.create(
            username="super2",
            telephone="70000016",
            role="superviseur"
        )

        self.tech_visible = Technicien.objects.create(
            nom="Visible",
            prenom="Tech",
            telephone="70000017",
            genre="M",
            superviseur=self.superviseur,
            actif=True
        )

        self.tech_hidden = Technicien.objects.create(
            nom="Hidden",
            prenom="Tech",
            telephone="70000018",
            genre="M",
            superviseur=self.other_superviseur,
            actif=True
        )

    def test_queryset_filtered_by_superviseur(self):

        form = AffectationTechnicienForm(
            superviseur=self.superviseur
        )

        queryset = form.fields["technicien"].queryset

        self.assertIn(
            self.tech_visible,
            queryset
        )

        self.assertNotIn(
            self.tech_hidden,
            queryset
        )