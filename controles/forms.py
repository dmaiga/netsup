from django import forms
from controles.models import ControleSite

class ControleSiteForm(forms.ModelForm):
    class Meta:
        model = ControleSite
        fields = [
            "techniciens_presents",
            "etat_proprete",
            "incident",
            "problemes",
            "observations",
            "photo_site",
            "photo_presence",
        ]
        widgets = {
            "techniciens_presents": forms.NumberInput(attrs={
                "class": "input input-bordered w-full font-bold text-center text-lg",
                "min": "0"
            }),
            "etat_proprete": forms.Select(attrs={
                "class": "select select-bordered w-full font-semibold"
            }),
            "incident": forms.CheckboxInput(attrs={
                "class": "toggle toggle-error toggle-lg"
            }),
            "observations": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full",
                "rows": "3",
                "placeholder": "Notes complémentaires..."
            }),
            "problemes": forms.Textarea(attrs={
                "class": "textarea textarea-bordered border-error w-full",
                "rows": "3",
                "placeholder": "Précisez la nature du problème..."
            }),
            "photo_site": forms.FileInput(attrs={
                "class": "file-input file-input-bordered file-input-primary w-full",
                "accept": "image/*",
                "capture": "environment"
            }),
            "photo_presence": forms.FileInput(attrs={
                "class": "file-input file-input-bordered file-input-secondary w-full",
                "accept": "image/*",
                "capture": "environment",
                "required": "required" # Ajout HTML5 obligatoire
            }),
        }

    def __init__(self, *args, **kwargs):
        # On récupère le site passé par la vue pour la validation
        self.site = kwargs.pop('site', None)
        super().__init__(*args, **kwargs)
        # Force le champ photo_presence à être obligatoire au niveau Django
        self.fields['photo_presence'].required = True
        self.fields['etat_proprete'].required = True

    def clean(self):
        cleaned_data = super().clean()
        
        presents = cleaned_data.get("techniciens_presents")
        incident = cleaned_data.get("incident")
        problemes = cleaned_data.get("problemes")
        photo_presence = cleaned_data.get("photo_presence")

        # 1. Validation : Photo présence obligatoire
        if not photo_presence:
            self.add_error("photo_presence", "La photo de la feuille de présence est obligatoire.")

        # 2. Validation : Comparaison avec le nombre prévu sur le site
        if self.site and presents is not None:
            prevus = self.site.nombre_techniciens_prevus
            if presents > prevus:
                self.add_error(
                    "techniciens_presents", 
                    f"Erreur : Le nombre de présents ({presents}) ne peut pas dépasser le nombre prévu ({prevus})."
                )

        # 3. Validation : Incident / Description
        if incident and not problemes:
            self.add_error("problemes", "La description est obligatoire en cas d'incident.")
            
        return cleaned_data