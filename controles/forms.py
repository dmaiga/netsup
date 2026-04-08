from django import forms
from django.forms import formset_factory
from controles.models import ControleSite, PointageAgent
from users.models import User,Technicien


class ControleSiteForm(forms.ModelForm):
    class Meta:
        model = ControleSite
        fields = [
            "etat_proprete",
            "incident",
            "problemes",
            "observations",
            "photo_site",
            
        ]
        widgets = {
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
                "placeholder": "Précisez la nature du problème (sécurité, propreté, matériel...)..."
            }),
            "photo_site": forms.FileInput(attrs={
                "class": "file-input file-input-bordered file-input-primary w-full",
                "accept": "image/*",
                "capture": "environment"
            }),
            
        }

    def __init__(self, *args, **kwargs):
        self.site = kwargs.pop('site', None)
        super().__init__(*args, **kwargs)
      
        self.fields['etat_proprete'].required = True

    def clean(self):
        cleaned_data = super().clean()
        incident = cleaned_data.get("incident")
        problemes = cleaned_data.get("problemes")


        if incident and not problemes:
            self.add_error("problemes", "La description est obligatoire en cas d'incident.")

        return cleaned_data


class PointageAgentForm(forms.Form):
    """
    Formulaire dynamique pour pointer UN agent (présent/absent + motif).
    Utilisé dans un formset dans la vue controle_site.
    """
    technicien_id = forms.IntegerField(widget=forms.HiddenInput())
    nom_affiche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "input input-sm w-full", "readonly": "readonly"})
    )
    present = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-success checkbox-lg"})
    )
    motif_absence = forms.ChoiceField(
        choices=PointageAgent.MOTIF_ABSENCE,
        required=False,
        widget=forms.Select(attrs={"class": "select select-bordered select-sm w-full"})
    )
    commentaire = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered input-sm w-full",
            "placeholder": "Commentaire optionnel..."
        })
    )
  

def build_pointage_formset(agents, data=None):
    """
    Construit un formset pré-rempli avec la liste des agents du site.
    """
    initial = [
        {
            "technicien_id": agent.id,
            "nom_affiche": f"{agent.prenom} {agent.nom}",
            "present": True,
        }
        for agent in agents
    ]
    PointageFormSet = formset_factory(PointageAgentForm, extra=0)
    if data:
        return PointageFormSet(data, initial=initial, prefix="pointage")
    return PointageFormSet(initial=initial, prefix="pointage")
