import cgi
import codecs
import csv
import pandas as pd

from django.shortcuts import render, redirect
from .forms import FormEntrada
from .models import Entrada
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.db.models import Avg, Count, Sum, Q
from django.http import JsonResponse, HttpResponse  # libreria para manejar json

from Dashboard.forms import CreateUserForm
from Dashboard.models import FactSaber11, DimTiempo
from Dashboard.models import DimEstudiantes
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import psycopg2, psycopg2.extras

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
@login_required(login_url='login')
def inicio(request):
    return render(request, "Dashboard/base_0.html")


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('obando')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('obando')
            else:
                messages.info(request, 'Usuario o Contraseña Incorrectos')

        context = {}
        return render(request, "Dashboard/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('obando')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Registro Exitoso para el Usuario: ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, "Dashboard/register.html", context)


@login_required(login_url='login')
def obando(request):
    return render(request, "Dashboard/obando.html")


@login_required(login_url='login')
def grafic(request):
    return render(request, "Dashboard/grafic.html")

@login_required(login_url='login')
def subir(request):
    if request.method == 'POST':
         form = FormEntrada(request.POST, request.FILES)
         if form.is_valid():

            encabezados = []
            insert = Entrada()
            insert.archivo = request.FILES.get('file')
            deli=request.POST.get('delimitador')
            insert.save()
            f = codecs.open('media/'+str(insert.archivo), encoding='utf-8',)
            f2 = open(str('media/icfes/data.txt'), 'a+')
            for line in f:
                f2.write(line.replace(deli,';'))
            f.close()
            f2.close()
            f2 = open(str('media/icfes/data.txt'), 'r')
            mensaje = f2.readline()
            print(mensaje)
            f2.close()
            df = pd.read_csv(str(BASE_DIR+'/media/icfes/data.txt'), encoding='unicode_escape', sep=";", dtype='unicode')
            df = df.drop(df[df['ESTU_DEPTO_PRESENTACION'] != 'NARIÑO'].index)
            df = df.drop(df[(df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152022000084') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152210000261') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152215000138') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152215000511') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152224000019') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152227000010') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152227000222') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152317000035') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152317000078') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152323000063') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152323000161') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000166') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000182') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000191') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000204') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000212') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000221') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000409') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000581') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356000735') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356001367') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152356001901') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152560000124') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152573000093') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152585000161') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152585000188') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152585000374') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '152585000439') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252210000096') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252215000035') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252215000451') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252215000469') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252224000145') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000057') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000138') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000162') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000189') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000791') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000863') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000880') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252227000936') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252287000218') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252317000081') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252317000404') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252317000412') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252323000190') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252352000069') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252352000140') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252352000166') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252352000263') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356000101') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356000535') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356000888') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356001001') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356001019') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356001035') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356001485') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252356001663') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252560000030') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252560000048') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252560000099') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252560000340') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252573000195') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252573000209') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '252585000352') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '286320001413') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352215000587') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352287000018') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000033') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000131') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000149') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000157') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000173') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356000467') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001048') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001421') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001561') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001819') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001927') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001951') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356001978') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '352356002001') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '452022000118') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '452215000441') &
                            (df['COLE_COD_DANE_ESTABLECIMIENTO'] != '452215000492') ].index)

            # df.columns = [c.lower() for c in df.columns]
            from sqlalchemy import create_engine
            engine = create_engine('postgresql://postgres:1234@localhost:5432/icfes-1')

            df.to_sql("table_temp", engine)
            # conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
            # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # # sql = "delete from table_temp where 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152022000084'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152210000261'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152215000138'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152215000511'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152224000019'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152227000010'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152227000222'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152317000035'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152317000078'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152323000063'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152323000161'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000166'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000182'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000191'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000204'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000212'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000221'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000409'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000581'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356000735'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356001367'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152356001901'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152560000124'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152573000093'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152585000161'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152585000188'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152585000374'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'152585000439'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252210000096'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252215000035'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252215000451'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252215000469'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252224000145'and  'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000057'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000138'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000162'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000189'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000308'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000791'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000863'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000880'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252227000936'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252287000218'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252317000081'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252317000404'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252317000412'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252323000190'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252352000069'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252352000140'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252352000166'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252352000263'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356000101'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356000535'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356000888'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356001001'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356001019'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356001035'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356001485'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252356001663'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252560000030'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252560000048'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252560000099'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252560000340'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252573000195'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252573000209'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'252585000352'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'286320001413'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352215000587'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352287000018'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000033'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000131'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000149'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000157'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000173'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356000467'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001048'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001421'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001561'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001819'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001927'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001951'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356001978'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'352356002001'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'452022000118'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'452215000441'and 'COLE_COD_DANE_ESTABLECIMIENTO'<>'452215000492';"
            # sql = "select 'COLE_CODIGO_ICFES' from table_temp where 'COLE_CODIGO_ICFES'='011502'"
            # cur.execute(sql)
            # row = cur.fetchall()
            # print(row)
            # cur.close()
            # conn.close()
            # print(df)
            return render(request, "Dashboard/subir.html")
         else:
             messages.error(request, "Error al procesar el formulario")
    else:
        return render(request, "Dashboard/subir.html")


@login_required(login_url='login')
def gestionHtml(request):
    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(cole_nombre_sede) from fact_saber11,dim_lugares,dim_instituciones where fact_saber11.id_lugar=dim_lugares.id_lugar and fact_saber11.id_institucion=dim_instituciones.id_institucion;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    inst = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(cole_mcpio_ubicacion) from dim_lugares;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    muni = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(ano) from dim_tiempo;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    ano = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(periodo) from dim_tiempo;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    periodo = row

    context = {
        'object': inst,
        'muni': muni,
        'ano': ano,
        'periodo': periodo,

    }
    return render(request, "Dashboard/gestion.html", context)


@login_required(login_url='login')
def Gestion(request):
    label = []
    dato = []
    contador = []
    # se obtiene todas las variables desde el html desde un form con el metodo get
    message = request.GET['municipio']
    puntaje = request.GET['puntaje']
    inst = request.GET['inst']
    ano = request.GET['ano']
    periodo = request.GET['periodo']
    if (ano == "TODOS"):
        if (message == "TODOS"):
            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg(puntaje),
                                                                                           conta=Count(
                                                                                               puntaje)).order_by(
                '-prom')
            for entry in result:
                label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                contador.append(entry['conta'])
        else:
            if (inst == "General"):
                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                 conta=Count(
                                                                                                     puntaje)).filter(
                    id_lugar__cole_mcpio_ubicacion=message).order_by('-prom')
            else:
                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                 conta=Count(
                                                                                                     puntaje)).filter(
                    id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by('-prom')
            for entry in result:
                label.append(entry['id_institucion__cole_nombre_sede'])  # guarda nombre del departamento ya agrupado
                dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por inst)
                contador.append(entry['conta'])
    else:
        if (periodo == 'TODOS'):
            if (message == "TODOS"):
                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg(puntaje),
                                                                                               conta=Count(
                                                                                                   puntaje)).filter(
                    id_tiempo__ano=ano).order_by('-prom')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                    dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                    contador.append(entry['conta'])
            else:
                if (inst == "General"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by('-prom')
                else:
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                        id_institucion__cole_nombre_sede=inst).order_by('-prom')
                for entry in result:
                    label.append(entry['id_institucion__cole_nombre_sede'])  # guarda nombre de departamento ya agrupado
                    dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por inst)
                    contador.append(entry['conta'])
        else:
            if (message == "TODOS"):
                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg(puntaje),
                                                                                               conta=Count(
                                                                                                   puntaje)).filter(
                    id_tiempo__periodo=periodo).order_by('-prom')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                    dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                    contador.append(entry['conta'])
            else:
                if (inst == "General"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__periodo=periodo).order_by('-prom')
                else:
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__periodo=periodo,
                        id_institucion__cole_nombre_sede=inst).order_by('-prom')
                for entry in result:
                    label.append(entry['id_institucion__cole_nombre_sede'])  # guarda nombre de departamento ya agrupado
                    dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por inst)
                    contador.append(entry['conta'])

    return JsonResponse(data={

        'labels': label,
        'data': dato,
        'conta': contador,
    })


@login_required(login_url='login')
def gestionCHtml(request):
    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(cole_nombre_sede) from fact_saber11,dim_lugares,dim_instituciones where fact_saber11.id_lugar=dim_lugares.id_lugar and fact_saber11.id_institucion=dim_instituciones.id_institucion;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    inst = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(cole_mcpio_ubicacion) from dim_lugares;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    muni = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(ano) from dim_tiempo;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    ano = row

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select distinct(periodo) from dim_tiempo;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    periodo = row

    context = {
        'object': inst,
        'muni': muni,
        'ano': ano,
        'periodo': periodo,

    }
    return render(request, "Dashboard/gestionC.html", context)


@login_required(login_url='login')
def GestionC(request):
    label = []
    dato = []

    # se obtiene todas las variables desde el html desde un form con el metodo get
    message = request.GET['municipio']
    categoria = request.GET['categoria']
    inst = request.GET['inst']
    ano = request.GET['ano']
    periodo = request.GET['periodo']
    if (ano == "TODOS"):
        if (message == "TODOS"):
            result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).order_by(categoria)
        else:
            if (inst == "General"):
                result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                    id_lugar__cole_mcpio_ubicacion=message).order_by(categoria)
            else:
                result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                    id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(categoria)
    else:
        if (periodo == 'TODOS'):
            if (message == "TODOS"):
                result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                    id_tiempo__ano=ano).order_by(categoria)
            else:
                if (inst == "General"):
                    result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(categoria)
                else:
                    result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                        id_institucion__cole_nombre_sede=inst).order_by(categoria)
        else:
            if (message == "TODOS"):
                result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                    id_tiempo__periodo=periodo).order_by(categoria)
            else:
                if (inst == "General"):
                    result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__periodo=periodo).order_by(categoria)
                else:
                    result = FactSaber11.objects.values(categoria).annotate(conta=Count('id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__periodo=periodo,
                        id_institucion__cole_nombre_sede=inst).order_by(categoria)

    for entry in result:
        label.append(entry[categoria])  # guarda nombre de la categoria segun corresponda
        dato.append(entry['conta'])  # guarda promedio de cada grupo creado(por inst o muni)

    return JsonResponse(data={

        'labels': label,
        'data': dato,
    })


@login_required(login_url='login')
def crear(request):
    return render(request, "Dashboard/crear.html")


@login_required(login_url='login')
def grafic_principal(request):
    label = []
    data = []
    contador = []

    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg('punt_global'),
                                                                                   conta=Count('punt_global')).order_by(
        '-prom')
    for entry in result:
        label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
        data.append(entry['prom'])  # guarda promedio de cada grupo creado(por departamento)
        contador.append(entry['conta'])

    result1 = FactSaber11.objects.all().aggregate(Count('id_estudiante'))
    # for entry in result1:
    #     conta = int(entry['id_estudiante__Count'])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    vari = 50
    sql = "select count(id_estudiante) from fact_saber11"
    # where id_estudiante>(%s)"
    # data = (vari, )
    cur.execute(sql)
    row = cur.fetchone()
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql2 = "select count(distinct cole_nombre_sede) from dim_instituciones"
    cur2.execute(sql2)
    row2 = cur2.fetchone()
    sql3 = "select count(distinct cole_mcpio_ubicacion) from dim_lugares "
    cur.execute(sql3)
    row3 = cur.fetchone()
    # for entry in cur.fetchone():
    #     muni.append(entry)
    cur.close()
    conn.close()
    conta = row[0]
    inst = row2[0]
    muni = row3[0]

    return JsonResponse(data={  # manda en tipo json los resultados
        'labels': label,
        'data': data,
        'conta': contador,
        'contador': conta,
        'instituciones': inst,
        'municipios': muni,
    })


@login_required(login_url='login')
def punt_anio(request):
    label = []
    puntaje = []

    result = FactSaber11.objects.values('id_tiempo__ano').annotate(Count('id_tiempo__ano'),
                                                                   prom=Avg('punt_global')).order_by('prom')
    for entry in result:
        puntaje.append(entry['prom'])
        label.append(entry['id_tiempo__ano'])

    return JsonResponse(data={
        'labels': label,
        'puntajes': puntaje
    })


@login_required(login_url='login')
def tot_est(request):
    label = []
    conta = []

    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
        Count('id_lugar__cole_mcpio_ubicacion'), conta=Count('id_estudiante'))
    for entry in result:
        label.append(entry['id_lugar__cole_mcpio_ubicacion'])
        conta.append(entry['conta'])
    return JsonResponse(data={
        'labels': label,
        'conta': conta,
    })


@login_required(login_url='login')
def critic_chart(request):  # vista donde se maneja la grafica y donde se fabrica el json
    label = []
    data = []

    # for labeles in Saberpro2012.objects.values_list('estu_colegiotermino_dept', flat=True).distinct('estu_colegiotermino_dept'): #consulta que agrupa todo lo repetido
    #     label.append(labeles)

    # for n in label:
    #     for i in Saberpro2012.objects.values('mod_lectura_critica'):
    #         datos=Saberpro2012.objects.values('mod_lectura_critica').filter(Q(label[n]='estu_colegiotermino_dept'))
    #         suma=0;
    #         conta=0;
    #         for entry in datos:
    #             suma+=entry['mod_lectura_critica']
    #             conta+=1
    #         data=suma/conta
    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg('punt_lec_crit')).order_by(
        '-prom')  # consulta que agrupa y saca promedio de lo agrupado con llaves foraneas
    for entry in result:  # cada vez que obtenga resultado de la consulta
        label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
        data.append(entry['prom'])  # guarda promedio de cada grupo creado(por departamento)

    return JsonResponse(data={  # manda en tipo json los resultados
        'labels': label,
        'data': data,
    })


@login_required(login_url='login')
def est_anio(request):
    label = []
    data = []
    porcen = []
    total = 0
    result = FactSaber11.objects.values('id_tiempo__ano').annotate(suma=Count('id_estudiante'))
    for entry in result:
        label.append(entry['id_tiempo__ano'])
        total += entry['suma']
        data.append(entry['suma'])

    for entry in result:
        porcentaje = round((entry['suma'] / total) * 100)
        porcen.append(porcentaje)

    return JsonResponse(data={
        'labels': label,
        'data': data,
        'porcen': porcen,
    })


@login_required(login_url='login')
def est_edad(request):
    label = []
    data = []
    result = DimEstudiantes.objects.values('estu_rango_edad').annotate(conta=Count('estu_rango_edad'))
    for entry in result:
        label.append(entry['estu_rango_edad'])
        data.append(int(entry['conta']))
    return JsonResponse(data={
        'labels': label,
        'data': data
    })


@login_required(login_url='login')
def desemp_ciu_edad(request):
    label = []
    avanzado = []
    # .filter(id_pru_soc_ciu__desemp_soc_ciu='MINIMO')
    satisfactorio = []
    minimo = []
    insuficiente = []
    desmp = []
    cont = []

    result = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='MINIMO')
    for entry in result:
        desmp.append(entry['id_pru_soc_ciu__desemp_soc_ciu'])
        label.append(entry['id_estudiante__estu_rango_edad'])
        minimo.append(entry['conta'])

    result2_1 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='AVANZADO').filter(id_estudiante__estu_rango_edad='MENORES DE 17')
    for entry in result2_1:
        avanzado.append(entry['conta'])

    result2_2 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='AVANZADO').filter(id_estudiante__estu_rango_edad='18 Y 19')

    for entry in result2_2:
        avanzado.append(entry['conta'])

    result2_3 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='AVANZADO').filter(id_estudiante__estu_rango_edad='20 A 28')

    for entry in result2_3:
        avanzado.append(entry['conta'])

    result2_4 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='AVANZADO').filter(id_estudiante__estu_rango_edad='17')

    for entry in result2_4:
        avanzado.append(entry['conta'])

    result2_5 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='AVANZADO').filter(id_estudiante__estu_rango_edad='MAYORES DE 28')

    for entry in result2_5:
        avanzado.append(entry['conta'])

    result3_1 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='SATISFACTORIO').filter(id_estudiante__estu_rango_edad='MENORES DE 17')
    for entry in result3_1:
        satisfactorio.append(entry['conta'])

    result3_2 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='SATISFACTORIO').filter(id_estudiante__estu_rango_edad='18 Y 19')

    for entry in result3_2:
        satisfactorio.append(entry['conta'])

    result3_3 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='SATISFACTORIO').filter(id_estudiante__estu_rango_edad='20 A 28')

    for entry in result3_3:
        satisfactorio.append(entry['conta'])

    result3_4 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='SATISFACTORIO').filter(id_estudiante__estu_rango_edad='17')

    for entry in result3_4:
        satisfactorio.append(entry['conta'])

    result3_5 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='SATISFACTORIO').filter(id_estudiante__estu_rango_edad='MAYORES DE 28')

    for entry in result3_5:
        satisfactorio.append(entry['conta'])

    result4_1 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='INSUFICIENTE').filter(id_estudiante__estu_rango_edad='MENORES DE 17')
    for entry in result4_1:
        insuficiente.append(entry['conta'])

    result4_2 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='INSUFICIENTE').filter(id_estudiante__estu_rango_edad='18 Y 19')

    for entry in result4_2:
        insuficiente.append(entry['conta'])

    result4_3 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='INSUFICIENTE').filter(id_estudiante__estu_rango_edad='20 A 28')

    for entry in result4_3:
        insuficiente.append(entry['conta'])

    result4_4 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='INSUFICIENTE').filter(id_estudiante__estu_rango_edad='17')

    for entry in result4_4:
        insuficiente.append(entry['conta'])

    result4_5 = FactSaber11.objects.values('id_pru_soc_ciu__desemp_soc_ciu', 'id_estudiante__estu_rango_edad').annotate(
        conta=Count('id_pru_soc_ciu__desemp_soc_ciu'), conta2=Count('id_estudiante__estu_rango_edad')).filter(
        id_pru_soc_ciu__desemp_soc_ciu='INSUFICIENTE').filter(id_estudiante__estu_rango_edad='MAYORES DE 28')

    for entry in result4_5:
        insuficiente.append(entry['conta'])

    return JsonResponse(data={
        'labels': label,
        'minimo': minimo,
        'avanzado': avanzado,
        'satisfactorio': satisfactorio,
        'insuficiente': insuficiente,

    })
