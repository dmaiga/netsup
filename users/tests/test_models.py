from django.test import TestCase
from users.models import User, Technicien


class UserModelTest(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            username="admin_test",
            password="password123",
            telephone="70000001",
            role="admin"
        )

        self.assertEqual(user.username, "admin_test")

        self.assertEqual(user.role, "admin")

        self.assertTrue(user.check_password("password123"))

    def test_full_name_property(self):

        user = User.objects.create(
            username="john",
            first_name="John",
            last_name="Doe",
            telephone="70000002",
            role="admin"
        )

        self.assertEqual(
            user.full_name,
            "John Doe"
        )

    def test_full_name_fallback_username(self):

        user = User.objects.create(
            username="fallback_user",
            telephone="70000003",
            role="admin"
        )

        self.assertEqual(
            user.full_name,
            "fallback_user"
        )


class TechnicienModelTest(TestCase):

    def setUp(self):

        self.superviseur = User.objects.create(
            username="superviseur1",
            telephone="70000004",
            role="superviseur"
        )

    def test_generate_matricule(self):

        technicien = Technicien.objects.create(
            nom="Diallo",
            prenom="Moussa",
            telephone="70000005",
            genre="M",
            superviseur=self.superviseur
        )

        self.assertTrue(
            technicien.matricule.startswith("TECH-")
        )

    def test_technicien_str(self):

        technicien = Technicien.objects.create(
            nom="Traore",
            prenom="Awa",
            telephone="70000006",
            genre="F",
            superviseur=self.superviseur
        )

        self.assertEqual(
            str(technicien),
            "Awa Traore"
        )

    def test_user_manager_excludes_deleted(self):
    
        User.objects.create(
            username="active_user",
            telephone="70000007",
            role="admin",
            is_deleted=False
        )
    
        User.objects.create(
            username="deleted_user",
            telephone="70000008",
            role="admin",
            is_deleted=True
        )
    
        users = User.objects.all()
    
        usernames = [user.username for user in users]
    
        self.assertIn("active_user", usernames)
    
        self.assertNotIn("deleted_user", usernames)
