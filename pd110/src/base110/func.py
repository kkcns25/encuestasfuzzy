# funciones auxiliares para views
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm, RegModelForm, EncuestaForm
import sys
import csv
from unidecode import unidecode
from django.conf.urls import url
from os import listdir
from os.path import isfile, join
from .models import Registrado
from pathlib import Path
import sqlite3
from sqlite3 import Error
import numpy as np

def datos(datos):
    datos = datos.split('?')
    if len(datos)>=2:
        datos = datos[2]
        return datos[:-2]
    else:
        return ''

def resultados(datos, len_q, len_d):
    datos_finales = np.zeros((len_q, 101),dtype='int32')

    def sumar_datos(dato, columna):
        dato = dato.split('/')
        try:
            d1 = int(dato[0])
            d2 = int(dato[1])

            n = 0
            while n <= 100:
                if (n >= d1 and n <= d2):
                    datos_finales[columna][n] += 1
                n += 1

        except:
            print( "Error en el tipo de dato.")#si hay algún dato que no se pueda convertir a int, capturamos la exception y el programa sigue funcionando

    for i in datos:
        col=0
        for j in i:
            sumar_datos(j, col)
            col +=1
    datos_finales = (datos_finales * 100 // len_d)  # multiplicamos por 100 y dividimos entre en numero de datos para obtener los resultados en %
    datos_finales = datos_finales.tolist()

    return(datos_finales)

def lista_encuestas():

    ruta = 'static_pro/static/csv/'
    carpeta = Path(ruta)

    def ls3(path):
        return [obj.name for obj in Path(path).iterdir() if obj.is_file()]

    return ls3(carpeta)

def encuesta_uploaded():
    ruta = '../static_env/media_root/static/csv/'
    print('entra')
    carpeta = Path(ruta)
    print('entra1')
    def ls3(path):
        return [obj.name for obj in Path(path).iterdir() if obj.is_file()]

    files = ls3(carpeta)

    return files[0]

def escribir_csv(encuesta, datos):

    csvsalida = open('static_pro/static/csv/' + encuesta, 'a', newline='')  # cambiamos el directorio a la carpeta donde se van a guardar los csv
    salida = csv.writer(csvsalida, delimiter='#')  # comenzamos a escribir la csv y cambiamos el delimitador para que sea almohadilla
    salida.writerow(datos)  # escribimos los datos
    del salida
    csvsalida.close()  # cerramos el csv

def leer_csv(nombre):
    file = open('static_pro/static/csv/' + nombre)
    reader = csv.reader(file, delimiter='#', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    questions = []
    for row in reader:
        questions.append(row)

    file.close()

    return questions

def leer_csv_uploaded(nombre):
    file = open('../static_env/media_root/static/csv/' + nombre)
    reader = csv.reader(file, delimiter='#', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    questions = []
    for row in reader:
        questions.append(row)
    file.close()

    return questions

def nombre_encuesta(nombre):

    nombre = nombre.replace('%20', ' ')
    nombre = nombre.split('?')

    if len(nombre)==2:
        nombre = nombre[1]
        nombre = nombre[:-2]

    else:
        if len(nombre)>2:
            nombre = nombre[1]
        else:
           nombre = ''

    return nombre


def crear_tabla(nombre):
    def sql_connection():
        try:
            con = sqlite3.connect('users.db')
            print('conexion establecida')
            return con

        except Error:
            print(Error)

        finally:
            con.close()
    def sql_table(con):
        con = sqlite3.connect('users.db')
        cursorOjt = con.cursor()
        cursorOjt.execute("CREATE TABLE if not exists '%s' (encuestas text)" %nombre)

        print('tabla creada')

    con = sql_connection()
    sql_table(con)

def escribir_tabla(nombre, encuesta):
    def sql_connection():
        try:
            con = sqlite3.connect('users.db')
            print('conexion establecida')
            return con

        except Error:
            print(Error)

        finally:
            con.close()
    def sql_table(con):
        con = sqlite3.connect('users.db')
        cursorOjt = con.cursor()
        cursorOjt.execute("CREATE TABLE if not exists '%s' (encuestas text)" %nombre)
        cursorOjt.execute("INSERT INTO '%s' VALUES ( ? )" %nombre,(encuesta,))
        print('tabla escrita')
        con.commit()
    con = sql_connection()
    sql_table(con)

def leer_tabla(nombre):

    def sql_connection():
        try:
            con = sqlite3.connect('users.db')
            print('conexion establecida')
            return con

        except Error:
            print(Error)

        finally:
            con.close()
    def sql_table(con):
        global encuestas_realizadas  #se pone el atributo global para poder leerla fuera de la función
        con = sqlite3.connect('users.db')
        cursorOjt = con.cursor()
        cursorOjt.execute("CREATE TABLE if not exists '%s' (encuestas text)" %nombre)
        #cursorOjt.execute("INSERT INTO '%s' VALUES ( ? )" %nombre)
        cursorOjt.execute("SELECT * FROM '%s'" %nombre)
        encuestas_realizadas = cursorOjt.fetchall()

        con.commit()
    con = sql_connection()
    sql_table(con)

    encuestas_rea = encuestas_realizadas
    posicion = 0
    while posicion < len(encuestas_rea):
        encuestas_rea[posicion]= str(encuestas_rea[posicion])
        encuestas_rea[posicion]= encuestas_rea[posicion][2:-3]
        #print(encuestas_rea[posicion])
        posicion += 1
    #print(encuestas_rea)
    return encuestas_rea

def comprobar_encuesta(nombre):
    encuestas = leer_tabla('encuestas')
    posicion = 0
    while posicion < len(encuestas):
        if nombre == encuestas_realizadas[posicion]:
            return False
        posicion += 1
    return True

def comparar_encuestas(encuestas, encuestas_realizadas):
    posicion = 0
    while posicion < len(encuestas):
        pos = 0
        while pos < len(encuestas_realizadas):
            if encuestas[posicion] == encuestas_realizadas[pos]:
                encuestas.pop(posicion)

            pos+=1
        posicion += 1
    return encuestas


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']

    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de archivo no válido.')





