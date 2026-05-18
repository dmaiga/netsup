from django import forms
from users.models import Technicien, User


class UserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full"
        }),
        required=False
    )

    class Meta:
        model = User

        fields = [
            "username",
            "telephone",
            "role",
            "photo",
            "password",
        ]

        widgets = {

            "username": forms.TextInput(attrs={
                "class": "input input-bordered w-full"
            }),

            "telephone": forms.TextInput(attrs={
                "class": "input input-bordered w-full"
            }),

            "role": forms.Select(attrs={
                "class": "select select-bordered w-full"
            }),

            "photo": forms.FileInput(attrs={
                "class": "file-input file-input-bordered w-full"
            }),

        }

# users/forms_technicien.py

class TechnicienTerrainForm(forms.ModelForm):

    class Meta:
        model = Technicien

        fields = [
            'nom',
            'prenom',
            'telephone',
            'genre',
            'photo',
        ]
        widgets = {

            "nom": forms.TextInput(attrs={
                "class": "input input-bordered w-full"
            }),

            "prenom": forms.TextInput(attrs={
                "class": "input input-bordered w-full"
            }),

            "telephone": forms.TextInput(attrs={
                "class": "input input-bordered w-full"
            }),

            "genre": forms.Select(attrs={
                "class": "select select-bordered w-full"
            }),

            "photo": forms.FileInput(attrs={
                "class": "file-input file-input-bordered w-full"
            }),

        }

class AffectationTechnicienForm(forms.Form):

    technicien = forms.ModelChoiceField(
        queryset=Technicien.objects.all()
    )
    
    def __init__(self, *args, superviseur=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['technicien'].queryset = (
            Technicien.objects.filter(
                superviseur=superviseur,
                actif=True
            )
        )

