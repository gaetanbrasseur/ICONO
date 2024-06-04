from django import forms
class FormulaireRecherche(forms.Form):
    image = forms.CharField(label='' , required=False)
    