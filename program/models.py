# models.py

from django.db import models

class Conversion(models.Model):
    DECIMAL = 'decimal'
    BINARY = 'binary'
    OCTAL = 'octal'
    HEXADECIMAL = 'hexadecimal'
    
    CHOICES = [
        (DECIMAL, 'Desimal'),
        (BINARY, 'Biner'),
        (OCTAL, 'Oktal'),
        (HEXADECIMAL, 'Heksadesimal'),
    ]
    
    pilihan_konversi = models.CharField(max_length=20, choices=CHOICES)
    decimal = models.IntegerField(blank=True, null=True)
    biner = models.CharField(max_length=64, blank=True, null=True)
    oktal = models.CharField(max_length=64, blank=True, null=True)
    heksadesimal = models.CharField(max_length=64, blank=True, null=True)
    field_name = models.CharField(max_length=100)  # Ganti dengan field yang sesuai

    def __str__(self):
        return f'Conversion {self.id}'
