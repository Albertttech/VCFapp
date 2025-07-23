from django import forms
from vcfviewer.models import VCFFile

class VCFFileForm(forms.ModelForm):
    class Meta:
        model = VCFFile
        fields = ['name', 'max_contacts']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter file name'}),
            'max_contacts': forms.NumberInput(attrs={'min': 1}),
        }
