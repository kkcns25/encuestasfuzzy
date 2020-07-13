from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages

from django.http import HttpResponseRedirect
from .forms import ContactForm, RegModelForm, EncuestaForm, UploadForm
import sys
import csv
import os
from unidecode import unidecode
from .func import *
from django.conf.urls import url
from os import listdir
from os.path import isfile, join
from .models import Registrado, Upload
from pathlib import Path
import sqlite3
from sqlite3 import Error


# Create your views here.
def inicio(request):
    return render(request, "inicio.html")


def contact(request):
    titulo = "Contacto"
    form = ContactForm(request.POST or None)
    if form.is_valid():

        form_email = form.cleaned_data.get("email")
        form_mensaje = form.cleaned_data.get("mensaje")
        form_nombre = form.cleaned_data.get("nombre")
        asunto = 'Form de contacto'
        email_from = settings.EMAIL_HOST_USER
        email_to = [form_email]#Cambiar a ver si funciona en produccion
        email_mensaje = "%s: %s enviado por %s" %(form_nombre, form_mensaje, form_email)

        send_mail(asunto,
                  email_mensaje,
                  email_from,
                  [email_to],
                  fail_silently=False
                  )
        return render(request, "inicio.html")
    context = {
        "form": form,
        "titulo": titulo,
    }

    return render(request, "forms.html", context)


def create(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encabezado = "Vamos a crear una encuesta, recuerda rellenar el título y al menos una pregunta."
        global problema
        problema = ''
        form = EncuestaForm(request.POST or None)

        context = {
            "form": form,
            "titulo": encabezado,
            "problema": problema
        }
        if form.is_valid():  #mientras el formulario no sea valido, estamos a espera, no hacemos nada
            nombre = unidecode(str(form.cleaned_data.get("titulo"))+".csv")#nombre de la encuesta, pasamos a unicode para eliminar posibles problemas con caracteres
            pregunta1 = str(form.cleaned_data.get("pregunta1"))
            pregunta2 = str(form.cleaned_data.get("pregunta2"))
            pregunta3 = str(form.cleaned_data.get("pregunta3"))
            pregunta4 = str(form.cleaned_data.get("pregunta4"))
            pregunta5 = str(form.cleaned_data.get("pregunta5"))
            pregunta6 = str(form.cleaned_data.get("pregunta6"))
            pregunta7 = str(form.cleaned_data.get("pregunta7"))
            pregunta8 = str(form.cleaned_data.get("pregunta8"))
            pregunta9 = str(form.cleaned_data.get("pregunta9"))
            pregunta10 = str(form.cleaned_data.get("pregunta10"))

            datos = [pregunta1, pregunta2,pregunta3, pregunta4, pregunta5, pregunta6, pregunta7, pregunta8, pregunta9, pregunta10]  #aqui hay que meter el nombre de            las peguntas que se han insertado por teclado
            posicion = 0
            nombre = nombre.replace("'", " ")#reemplazamos las posibles comillas y acentos que pueda haber
            nombre = nombre.replace('"', ' ')
            nombre = nombre.replace(',', ' ')#reemplazamos las posibles comillas y acentos que pueda haber
            nombre = nombre.replace('?', '¿')#reemplazamos las posibles comillas y acentos que pueda haber
            nombre = nombre.replace('#', ' ')#reemplazamos las posibles comillas y acentos que pueda haber
            while posicion < len(datos):
                if datos[posicion] == 'None':
                    datos.pop(posicion)
                else:
                    datos[posicion] = datos[posicion].replace("#", " ")
                    posicion = posicion + 1

            # se puede hacer una comprobación para que ninguna pregunta, osea en datos, no hay ninguna almohadilla
            # hay que poner algo para que el titulo no pueda estar en blanco, da fallo

            if comprobar_encuesta(nombre) == False: #comprobamos si ya existe otra encuesta con el mismo nombre
                problema = 'Por favor introduce otro título, ya existe una encuesta con este título'
                context = {
                    "form": form,
                    "titulo": encabezado,
                    "problema": problema
                }
                return render(request, "create.html", context)


            if (len(datos) != 0) and (nombre!='None.csv') and (comprobar_encuesta(nombre) == True):# si no se introduce ningnua pregunta y titulo no nos deja crear la encuesta
                escribir_tabla('encuestas', nombre)
                csvsalida = open('static_pro/static/csv/'+nombre, 'w',newline='')  # cambiamos el directorio a la carpeta donde se van a guardar los csv
                salida = csv.writer(csvsalida,delimiter='#')#comenzamos a escribir la csv y cambiamos el delimitador para que sea doble almohadilla
                salida.writerow(datos) #escribimos los datos
                del salida
                csvsalida.close()#cerramos el csv
                print('encuesta ok')
                return render(request, "created.html", context)

        return render(request, "create.html", context)


def profile(request):

    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encuestas_realizadas = leer_tabla(request.user)

        encuestas = comparar_encuestas(lista_encuestas(), encuestas_realizadas)
        if len(encuestas) == 0:
            encuestas = ''

        context = {
            "files": encuestas,
        }
        return render(request, "profile.html", context)



def slider_q(request):
 # codigo django necesario para contestar la pregunta, pro si es necesario
    encabezado = "Nombre de la encuesta: "
    nombre = nombre_encuesta(str(request))
    print(nombre)

    encabezado= encabezado + nombre[:-4] #quitamos '.csv' al nombre de la encuesta

    if nombre=='':
        return render(request, "warning.html")

    datos = leer_csv(nombre)
    questions = datos[0] #nos quedamos sólo con la primera fila, que va a ser la lista de preguntas

    context = {
        "titulo": encabezado,
        "questions": questions,
        "encuesta": nombre
    }
    return render(request, "slider.html", context)

def start_q(request):
 # codigo django necesario para contestar la pregunta, pro si es necesario
    return render(request, "start_q.html")

def sure(request):
 # codigo django necesario para contestar la pregunta, pro si es necesario
    return render(request, "sure.html")

def warning(request):
 # codigo django necesario para contestar la pregunta, pro si es necesario
    return render(request, "warning.html")

def finished(request):
    encuesta = nombre_encuesta(str(request))
    dato = datos(str(request))
    dato = dato.split(',')

    if encuesta != '':
        crear_tabla(request.user)
        escribir_tabla(request.user, encuesta)
        escribir_csv(encuesta, dato)

        return render(request, "finished.html")
    else:
        return render(request, "warning.html")

def viewresult(request):
    encabezado = "Por favor, elija la encuesta de la cual quiere ver los resultados:"
    encuestas = lista_encuestas()
    if len(encuestas) == 0:
        encabezado =" Lo sentimos, no hay ninguna encuestas para ver los resultados"
    context = {
        "titulo": encabezado,
        "encuestas": encuestas
    }
    return render(request, "viewresult.html", context)

def download(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encabezado = "Por favor, elija la encuesta que quiere descargar:"
        encuestas = lista_encuestas()
        if len(encuestas) == 0:
            encabezado =" Lo sentimos, no hay ninguna encuesta para descargar"
        context = {
            "titulo": encabezado,
            "encuestas": encuestas
        }
        return render(request, "download.html", context)


def delete(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encabezado = "Por favor, elija la encuesta que quiere borrar:"
        encuestas = lista_encuestas()
        if len(encuestas) == 0:
            encabezado =" Lo sentimos, no hay ninguna encuesta para borrar"
        context = {
            "titulo": encabezado,
            "encuestas": encuestas
        }
        return render(request, "delete.html", context)

def start_r(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        return render(request, "start_r.html")

def read_r(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        # codigo django necesario para leer los resultados del archivo csv
        encabezado = "Encuesta: "
        nombre = nombre_encuesta(str(request))
        encabezado = encabezado + nombre[:-4] #quitamos '.csv' al nombre de la encuesta

        if nombre=='':
            return render(request, "warning.html")

        datos = leer_csv(nombre)
        questions = datos[0] #nos quedamos sólo con la primera fila, que va a ser la lista de preguntas
        datos.pop(0) #eliminamos la fila de las pregutas, ya que ya la tenemos guardadad

        if len(datos)== 0:
            encabezado = 'Lo sentimos, esta encuesta todavía no tiene resultados'
            context = {
                "titulo": encabezado
            }
            return render(request, "warning.html", context)
        else:
            datos_finales = resultados(datos, len(questions), len(datos))

            context = {
                "titulo": encabezado,
                "questions": questions,
                "encuesta": nombre,
                "resultados": datos_finales
            }
            return render(request, "read_r.html", context)



def deleted(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encabezado = "Gracias, encuesta borrada."
        nombre = nombre_encuesta(str(request))
        if nombre == '':
            return render(request, "inicio.html", {})

        try:
            os.remove('static_pro/static/csv/' + nombre)
            print("% s removed successfully" % nombre)
        except OSError as error:
            print(error)
            print("File path can not be removed")
            encabezado = 'Encuesta no encontrada, no se ha podido borrar la encuesta.'

        context = {
            "titulo": encabezado,
        }
        return render(request, "deleted.html", context)

def upload(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        encabezado = "Por favor, suba una encuesta."

        archivo = UploadForm(request.POST, request.FILES)

        if (request.method == 'POST' and len(str(request.FILES))>20): #Comprobamos que se pulsa el boton y que se ha subido un archivo

            if archivo.is_valid():
                 archivo = request.FILES['archivo']
                 insert = Upload(archivo=archivo)
                 insert.save()
                 return read_r_uploaded(request)

        context = {
            "titulo": encabezado,
            "form": archivo
        }

        return render(request, "upload.html", context)


def read_r_uploaded(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, "inicio.html")
    else:
        # codigo django necesario para leer los resultados del archivo csv
        encabezado = "Encuesta: "
        nombre = str(encuesta_uploaded())
        encabezado = encabezado + nombre[:-4] #quitamos '.csv' al nombre de la encuesta

        if nombre == '':
            encabezado = 'Lo sentimos ha habido un fallo con la encuesta'
            context = {
                "titulo": encabezado
            }
            return render(request, "warning.html", context)

        datos = leer_csv_uploaded(nombre)
        questions = datos[0] #nos quedamos sólo con la primera fila, que va a ser la lista de preguntas
        datos.pop(0) #eliminamos la fila de las pregutas, ya que ya la tenemos guardadad

        try:
            os.remove('../static_env/media_root/static/csv/' + nombre)
            print("% s removed successfully" % nombre)
        except OSError as error:
            print(error)
            print("File path can not be removed")

        if len(datos) == 0:
            encabezado = 'Lo sentimos esta encuesta no tiene  resultados'
            context = {
                "titulo": encabezado
            }
            return render(request, "warning.html", context)
        else:
            datos_finales = resultados(datos, len(questions), len(datos))

            if datos_finales == '0':
                encabezado = 'Lo sentimos los resultados de la encuesta están corruptos'
                context = {
                    "titulo": encabezado
                }
                return render(request, "warning.html", context)

            context = {
                "titulo": encabezado,
                "questions": questions,
                "encuesta": nombre,
                "resultados": datos_finales
            }
            return render(request, "read_r_uploaded.html", context)



