from django import forms
from users.models import User


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