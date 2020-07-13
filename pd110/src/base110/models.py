from django.db import models
from django import forms
import os
#from .func import validate_file_extension

# Create your models here.
class Registrado(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

class Upload(models.Model):
    def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Por favor suba un archivo .csv válido")

    archivo = models.FileField(upload_to="static/csv",validators=[validate_file_extension], null=True, blank=True)

class Encuesta(models.Model):
    titulo = models.CharField(max_length=400, blank=True, null=True)
    pregunta1 = models.CharField(max_length=400, blank=True, null=True)
    pregunta2 = models.CharField(max_length=400, blank=True, null=True)
    pregunta3 = models.CharField(max_length=400, blank=True, null=True)
    pregunta4 = models.CharField(max_length=400, blank=True, null=True)
    pregunta5 = models.CharField(max_length=400, blank=True, null=True)
    pregunta6 = models.CharField(max_length=400, blank=True, null=True)
    pregunta7 = models.CharField(max_length=400, blank=True, null=True)
    pregunta8 = models.CharField(max_length=400, blank=True, null=True)
    pregunta9 = models.CharField(max_length=400, blank=True, null=True)
    pregunta10 = models.CharField(max_length=400, blank=True, null=True)


    def __unicode__(self): #Python 2
        return self.email

    def __str__(self): #python 3
        return self.email

