from django import forms
from django.forms import ClearableFileInput
from .models import Registrado
from .models import Encuesta
from .models import Upload

class RegModelForm(forms.ModelForm):
    class Meta:
        model = Registrado
        fields = ["nombre", "email"]


    def clean_email(self):# validacion correo de la uclm
        email = self.cleaned_data.get("email")
        email_base, proveedor = email.split("@")

        if not "uclm" in proveedor:
            raise forms.ValidationError("Por favor utiliza un correo con extension .uclm")
        return email

    def clean_nombre(self):  #validacion nombre
        nombre = self.cleaned_data.get("nombre ")
        #validaciones para el nombre
        return nombre


class ContactForm(forms.Form):
    nombre = forms.CharField(required=False)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

class EncuestaForm(forms.ModelForm):

    class Meta:
        model = Encuesta
        fields = ["titulo", "pregunta1", "pregunta2", "pregunta3", "pregunta4", "pregunta5", "pregunta6", "pregunta7", "pregunta8", "pregunta9", "pregunta10",]

class CustomClearableFileInput(ClearableFileInput):
        template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

class UploadForm(forms.ModelForm):


    class Meta:
        model = Upload
        fields = ('archivo',)
        widgets = {
            'archivo': CustomClearableFileInput
        }


