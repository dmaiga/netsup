from django import forms
from .models import Site

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'nom',
            'code_site',
            'adresse',
            'client_nom',
            'nombre_techniciens_prevus',
            'latitude',
            'longitude',
            'superviseur',
            'actif'
        ]

        widgets = {
            'nom': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'code_site': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'client_nom': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),

            'adresse': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 2
            }),

            'nombre_techniciens_prevus': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full'
            }),

            'latitude': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': 'any'
            }),

            'longitude': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': 'any'
            }),

            'superviseur': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),

            'actif': forms.CheckboxInput(attrs={
                'class': 'toggle toggle-primary'
            }),
        }