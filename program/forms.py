# forms.py

from django import forms
from .models import Conversion

class ConversionForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ['pilihan_konversi', 'field_name']
        labels = {
            'field_name': 'Masukkan Angka',
        }
