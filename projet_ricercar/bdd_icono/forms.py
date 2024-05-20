from django import forms
from bdd_icono.models import *
class FormulaireRecherche(forms.Form):
    image = forms.CharField(label='' , required=False)
    