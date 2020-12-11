import cgi
import codecs
import csv
import pandas as pd
from django.db.models.functions import Round

from django.shortcuts import render, redirect
import numpy as np
from Dashboard.decorators import unauthenticated_user, allowed_users
from Dashboard.forms import FormEntrada
from Dashboard.models import Entrada
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.db.models import Avg, Count, Sum, Q, Func
from django.http import JsonResponse, HttpResponse  # libreria para manejar json

from Dashboard.forms import CreateUserForm
from Dashboard.models import FactSaber11, DimTiempo
from Dashboard.models import DimEstudiantes
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import psycopg2, psycopg2.extras
from Dashboard import views

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Round(Func):
 function = 'ROUND'
 template='%(function)s(%(expressions)s, 2)'

@login_required(login_url='login')
def generalDashboard(request):
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
    sql = "select distinct(ano) from dim_tiempo order by ano;"
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
    return render(request, "Dashboard/generalDashboard.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def Dashboard(request):
    label = []
    dato = []
    contador = []
    categoria1 = []
    masculino = []
    Cmasculino = []
    femenino = []
    Cfemenino = []
    ticbuena = []
    Cticbuena = []
    ticregular = []
    Cticregular = []
    ticmala = []
    Cticmala = []
    Hmedio = []
    CHmedio = []
    Hcritico = []
    CHcritico = []
    Hsin = []
    CHsin = []
    e17 = []
    Ce17 = []
    e18y19 = []
    Ce18y19 = []
    e20a28 = []
    Ce20a28 = []
    emayoresde28 = []
    Cemayoresde28 = []
    emenoresde17 = []
    Cemenoresde17 = []
    es1 = []
    Ces1 = []
    es2 = []
    Ces2 = []
    es3 = []
    Ces3 = []
    es4 = []
    Ces4 = []
    es5 = []
    Ces5 = []
    es6 = []
    Ces6 = []
    EPC = []
    CEPC = []
    EPI = []
    CEPI = []
    ETC = []
    CETC = []
    ETI = []
    CETI = []
    n = []
    Cn = []
    nosabe = []
    Cnosabe = []
    postgrado = []
    Cpostgrado = []
    PC = []
    CPC = []
    PI = []
    CPI = []
    BC = []
    CBC = []
    BI = []
    CBI = []
    contad = []
    # se obtiene todas las variables desde el html desde un form con el metodo get
    message = request.GET['municipio']
    puntaje = request.GET['puntaje']
    inst = request.GET['inst']
    ano = request.GET['ano']
    categoria = request.GET['categoria']

    if (ano == "TODOS"):
        if (message == "TODOS"):
            if(categoria == "Genero"):

                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                    prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                    prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).order_by(
                    'id_lugar__cole_mcpio_ubicacion')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                    femenino.append(entry['prom1'])
                    masculino.append(entry['prom2'])
                    Cfemenino.append(entry['conta1'])
                    Cmasculino.append(entry['conta2'])
            else:
                if(categoria=="Condicion de las TIC"):

                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                        conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).order_by(
                        'id_lugar__cole_mcpio_ubicacion')
                    for entry in result:
                        label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                        ticbuena.append(entry['prom1'])
                        Cticbuena.append(entry['conta1'])
                        ticregular.append(entry['prom2'])
                        Cticregular.append(entry['conta2'])
                        ticmala.append(entry['prom3'])
                        Cticmala.append(entry['conta3'])

                else:
                    if(categoria=="Condicion en la que vive"):

                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).order_by(
                            'id_lugar__cole_mcpio_ubicacion')
                        for entry in result:
                            label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                            Hmedio.append(entry['prom1'])
                            CHmedio.append(entry['conta1'])
                            Hcritico.append(entry['prom2'])
                            CHcritico.append(entry['conta2'])
                            Hsin.append(entry['prom3'])
                            CHsin.append(entry['conta3'])

                    else:
                        if(categoria=="Rango de Edad"):

                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                conta4=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                conta5=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).order_by(
                                'id_tiempo__ano','id_lugar__cole_mcpio_ubicacion')
                            for entry in result:
                                label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                e17.append(entry['prom1'])
                                Ce17.append(entry['conta1'])
                                e18y19.append(entry['prom2'])
                                Ce18y19.append(entry['conta2'])
                                e20a28.append(entry['prom3'])
                                Ce20a28.append(entry['conta3'])
                                emayoresde28.append(entry['prom4'])
                                Cemayoresde28.append(entry['conta4'])
                                emenoresde17.append(entry['prom5'])
                                Cemenoresde17.append(entry['conta5'])

                        else:
                            if(categoria=="Estrato"):

                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                    prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                    prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                    prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                    prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                    conta4=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                    conta5=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                    conta6=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="6"))).order_by(
                                    'id_lugar__cole_mcpio_ubicacion')
                                for entry in result:
                                    label.append(
                                        entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                    es1.append(entry['prom1'])
                                    Ces1.append(entry['conta1'])
                                    es2.append(entry['prom2'])
                                    Ces2.append(entry['conta2'])
                                    es3.append(entry['prom3'])
                                    Ces3.append(entry['conta3'])
                                    es4.append(entry['prom4'])
                                    Ces4.append(entry['conta4'])
                                    es5.append(entry['prom5'])
                                    Ces5.append(entry['conta5'])
                                    es6.append(entry['prom6'])
                                    Ces6.append(entry['conta6'])
                            else:
                                if(categoria == "Nivel Educativo Padres"):

                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                        prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                        prom7=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                        prom8=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                        prom9=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                        prom10=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                        prom11=Round(Avg(puntaje, filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                        conta1=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                        conta6=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                        conta7=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                        conta8=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                        conta9=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                        conta10=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                        conta11=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                        ).order_by(
                                        'id_lugar__cole_mcpio_ubicacion')
                                    for entry in result:
                                        label.append(
                                            entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                        n.append(entry['prom1'])
                                        Cn.append(entry['conta1'])
                                        PI.append(entry['prom2'])
                                        CPI.append(entry['conta2'])
                                        PC.append(entry['prom3'])
                                        CPC.append(entry['conta3'])
                                        BI.append(entry['prom4'])
                                        CBI.append(entry['conta4'])
                                        BC.append(entry['prom5'])
                                        CBC.append(entry['conta5'])
                                        ETI.append(entry['prom6'])
                                        CETI.append(entry['conta6'])
                                        ETC.append(entry['prom7'])
                                        CETC.append(entry['conta7'])
                                        EPI.append(entry['prom8'])
                                        CEPI.append(entry['conta8'])
                                        EPC.append(entry['prom9'])
                                        CEPC.append(entry['conta9'])
                                        postgrado.append(entry['prom10'])
                                        Cpostgrado.append(entry['conta10'])
                                        nosabe.append(entry['prom11'])
                                        Cnosabe.append(entry['conta11'])

        else:
            if (inst == "General"):
                if (categoria == "Genero"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede','id_tiempo__ano').annotate(
                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message).order_by('id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede']+" : "+entry['id_tiempo__ano'])
                        femenino.append(entry['prom1'])
                        masculino.append(entry['prom2'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])

                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                            ticbuena.append(entry['prom1'])
                            Cticbuena.append(entry['conta1'])
                            ticregular.append(entry['prom2'])
                            Cticregular.append(entry['conta2'])
                            ticmala.append(entry['prom3'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                                conta1=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                conta2=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                id_lugar__cole_mcpio_ubicacion=message).order_by(
                                'id_institucion__cole_nombre_sede')
                            for entry in result:
                                label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                Hmedio.append(entry['prom1'])
                                CHmedio.append(entry['conta1'])
                                Hcritico.append(entry['prom2'])
                                CHcritico.append(entry['conta2'])
                                Hsin.append(entry['prom3'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                    prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                    prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                    prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                    conta4=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                    conta5=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                    id_lugar__cole_mcpio_ubicacion=message).order_by(
                                    'id_tiempo__ano', 'id_institucion__cole_nombre_sede')
                                for entry in result:
                                    label.append(
                                        entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                    e17.append(entry['prom1'])
                                    Ce17.append(entry['conta1'])
                                    e18y19.append(entry['prom2'])
                                    Ce18y19.append(entry['conta2'])
                                    e20a28.append(entry['prom3'])
                                    Ce20a28.append(entry['conta3'])
                                    emayoresde28.append(entry['prom4'])
                                    Cemayoresde28.append(entry['conta4'])
                                    emenoresde17.append(entry['prom5'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                        prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                        conta1=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                        conta6=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="6"))).filter(
                                        id_lugar__cole_mcpio_ubicacion=message).order_by(
                                        'id_institucion__cole_nombre_sede')
                                    for entry in result:
                                        label.append(
                                            entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                        es1.append(entry['prom1'])
                                        Ces1.append(entry['conta1'])
                                        es2.append(entry['prom2'])
                                        Ces2.append(entry['conta2'])
                                        es3.append(entry['prom3'])
                                        Ces3.append(entry['conta3'])
                                        es4.append(entry['prom4'])
                                        Ces4.append(entry['conta4'])
                                        es5.append(entry['prom5'])
                                        Ces5.append(entry['conta5'])
                                        es6.append(entry['prom6'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
                                            prom1=Round(Avg(puntaje,
                                                      filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                            prom2=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                            prom3=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                            prom4=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                            prom5=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                            prom6=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                            prom7=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                            prom8=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom9=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom10=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                            prom11=Round(Avg(puntaje,
                                                       filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                            conta1=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                            conta2=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                            conta3=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                            conta4=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                            conta5=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                            conta6=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                            conta7=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                            conta8=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta9=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta10=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                            conta11=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                            ).filter(
                                            id_lugar__cole_mcpio_ubicacion=message).order_by(
                                                'id_institucion__cole_nombre_sede')
                                        for entry in result:
                                            label.append(
                                                entry['id_institucion__cole_nombre_sede'] + " : " + entry[
                                                    'id_tiempo__ano'])
                                            n.append(entry['prom1'])
                                            Cn.append(entry['conta1'])
                                            PI.append(entry['prom2'])
                                            CPI.append(entry['conta2'])
                                            PC.append(entry['prom3'])
                                            CPC.append(entry['conta3'])
                                            BI.append(entry['prom4'])
                                            CBI.append(entry['conta4'])
                                            BC.append(entry['prom5'])
                                            CBC.append(entry['conta5'])
                                            ETI.append(entry['prom6'])
                                            CETI.append(entry['conta6'])
                                            ETC.append(entry['prom7'])
                                            CETC.append(entry['conta7'])
                                            EPI.append(entry['prom8'])
                                            CEPI.append(entry['conta8'])
                                            EPC.append(entry['prom9'])
                                            CEPC.append(entry['conta9'])
                                            postgrado.append(entry['prom10'])
                                            Cpostgrado.append(entry['conta10'])
                                            nosabe.append(entry['prom11'])
                                            Cnosabe.append(entry['conta11'])
            else:
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede', 'id_tiempo__ano').annotate(
                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by('id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                        femenino.append(entry['prom1'])
                        masculino.append(entry['prom2'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                            ticbuena.append(entry['prom1'])
                            Cticbuena.append(entry['conta1'])
                            ticregular.append(entry['prom2'])
                            Cticregular.append(entry['conta2'])
                            ticmala.append(entry['prom3'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                                conta1=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                conta2=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                                'id_institucion__cole_nombre_sede')
                            for entry in result:
                                label.append(
                                    entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                Hmedio.append(entry['prom1'])
                                CHmedio.append(entry['conta1'])
                                Hcritico.append(entry['prom2'])
                                CHcritico.append(entry['conta2'])
                                Hsin.append(entry['prom3'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                    prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                    prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                    prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                    conta4=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                    conta5=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                    id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                                    'id_tiempo__ano', 'id_institucion__cole_nombre_sede')
                                for entry in result:
                                    label.append(
                                        entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                    e17.append(entry['prom1'])
                                    Ce17.append(entry['conta1'])
                                    e18y19.append(entry['prom2'])
                                    Ce18y19.append(entry['conta2'])
                                    e20a28.append(entry['prom3'])
                                    Ce20a28.append(entry['conta3'])
                                    emayoresde28.append(entry['prom4'])
                                    Cemayoresde28.append(entry['conta4'])
                                    emenoresde17.append(entry['prom5'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                        prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                        conta1=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                        conta6=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="6"))).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                                        'id_institucion__cole_nombre_sede')
                                    for entry in result:
                                        label.append(
                                            entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                        es1.append(entry['prom1'])
                                        Ces1.append(entry['conta1'])
                                        es2.append(entry['prom2'])
                                        Ces2.append(entry['conta2'])
                                        es3.append(entry['prom3'])
                                        Ces3.append(entry['conta3'])
                                        es4.append(entry['prom4'])
                                        Ces4.append(entry['conta4'])
                                        es5.append(entry['prom5'])
                                        Ces5.append(entry['conta5'])
                                        es6.append(entry['prom6'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
                                            prom1=Round(Avg(puntaje,
                                                      filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                            prom2=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                            prom3=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                            prom4=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                            prom5=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                            prom6=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                            prom7=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                            prom8=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom9=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom10=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                            prom11=Round(Avg(puntaje,
                                                       filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                            conta1=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                            conta2=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                            conta3=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                            conta4=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                            conta5=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                            conta6=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                            conta7=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                            conta8=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta9=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta10=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                            conta11=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                        ).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                                            'id_institucion__cole_nombre_sede')
                                        for entry in result:
                                            label.append(
                                                entry['id_institucion__cole_nombre_sede'] + " : " + entry[
                                                    'id_tiempo__ano'])
                                            n.append(entry['prom1'])
                                            Cn.append(entry['conta1'])
                                            PI.append(entry['prom2'])
                                            CPI.append(entry['conta2'])
                                            PC.append(entry['prom3'])
                                            CPC.append(entry['conta3'])
                                            BI.append(entry['prom4'])
                                            CBI.append(entry['conta4'])
                                            BC.append(entry['prom5'])
                                            CBC.append(entry['conta5'])
                                            ETI.append(entry['prom6'])
                                            CETI.append(entry['conta6'])
                                            ETC.append(entry['prom7'])
                                            CETC.append(entry['conta7'])
                                            EPI.append(entry['prom8'])
                                            CEPI.append(entry['conta8'])
                                            EPC.append(entry['prom9'])
                                            CEPC.append(entry['conta9'])
                                            postgrado.append(entry['prom10'])
                                            Cpostgrado.append(entry['conta10'])
                                            nosabe.append(entry['prom11'])
                                            Cnosabe.append(entry['conta11'])


    else:
            if (message == "TODOS"):
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_tiempo__ano=ano).order_by(
                        'id_lugar__cole_mcpio_ubicacion')
                    for entry in result:
                        label.append(entry['id_lugar__cole_mcpio_ubicacion'])
                        femenino.append(entry['prom1'])
                        masculino.append(entry['prom2'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_tiempo__ano=ano).order_by(
                            'id_lugar__cole_mcpio_ubicacion')
                        for entry in result:
                            label.append(entry['id_lugar__cole_mcpio_ubicacion'])
                            ticbuena.append(entry['prom1'])
                            Cticbuena.append(entry['conta1'])
                            ticregular.append(entry['prom2'])
                            Cticregular.append(entry['conta2'])
                            ticmala.append(entry['prom3'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                                conta1=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                conta2=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                id_tiempo__ano=ano).order_by(
                                'id_lugar__cole_mcpio_ubicacion')
                            for entry in result:
                                label.append(entry['id_lugar__cole_mcpio_ubicacion'])
                                Hmedio.append(entry['prom1'])
                                CHmedio.append(entry['conta1'])
                                Hcritico.append(entry['prom2'])
                                CHcritico.append(entry['conta2'])
                                Hsin.append(entry['prom3'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                    prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                    prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                    prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                    conta4=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                    conta5=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                    id_tiempo__ano=ano).order_by(
                                    'id_tiempo__ano', 'id_lugar__cole_mcpio_ubicacion')
                                for entry in result:
                                    label.append(
                                        entry['id_lugar__cole_mcpio_ubicacion'])
                                    e17.append(entry['prom1'])
                                    Ce17.append(entry['conta1'])
                                    e18y19.append(entry['prom2'])
                                    Ce18y19.append(entry['conta2'])
                                    e20a28.append(entry['prom3'])
                                    Ce20a28.append(entry['conta3'])
                                    emayoresde28.append(entry['prom4'])
                                    Cemayoresde28.append(entry['conta4'])
                                    emenoresde17.append(entry['prom5'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                        prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                        conta1=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                        conta6=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_estrato_vivienda="6"))).filter(
                                        id_tiempo__ano=ano).order_by(
                                        'id_lugar__cole_mcpio_ubicacion')
                                    for entry in result:
                                        label.append(
                                            entry['id_lugar__cole_mcpio_ubicacion'])
                                        es1.append(entry['prom1'])
                                        Ces1.append(entry['conta1'])
                                        es2.append(entry['prom2'])
                                        Ces2.append(entry['conta2'])
                                        es3.append(entry['prom3'])
                                        Ces3.append(entry['conta3'])
                                        es4.append(entry['prom4'])
                                        Ces4.append(entry['conta4'])
                                        es5.append(entry['prom5'])
                                        Ces5.append(entry['conta5'])
                                        es6.append(entry['prom6'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                            'id_tiempo__ano').annotate(
                                            prom1=Round(Avg(puntaje,
                                                      filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                            prom2=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                            prom3=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                            prom4=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                            prom5=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                            prom6=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                            prom7=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                            prom8=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom9=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                            prom10=Round(Avg(puntaje, filter=Q(
                                                id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                            prom11=Round(Avg(puntaje,
                                                       filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                            conta1=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                            conta2=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                            conta3=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                            conta4=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                            conta5=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                            conta6=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                            conta7=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                            conta8=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta9=Count('id_estudiante',
                                                         filter=Q(
                                                             id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                            conta10=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                            conta11=Count('id_estudiante',
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                            ).filter(
                                            id_tiempo__ano=ano).order_by(
                                            'id_lugar__cole_mcpio_ubicacion')
                                        for entry in result:
                                            label.append(
                                                entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry[
                                                    'id_tiempo__ano'])
                                            n.append(entry['prom1'])
                                            Cn.append(entry['conta1'])
                                            PI.append(entry['prom2'])
                                            CPI.append(entry['conta2'])
                                            PC.append(entry['prom3'])
                                            CPC.append(entry['conta3'])
                                            BI.append(entry['prom4'])
                                            CBI.append(entry['conta4'])
                                            BC.append(entry['prom5'])
                                            CBC.append(entry['conta5'])
                                            ETI.append(entry['prom6'])
                                            CETI.append(entry['conta6'])
                                            ETC.append(entry['prom7'])
                                            CETC.append(entry['conta7'])
                                            EPI.append(entry['prom8'])
                                            CEPI.append(entry['conta8'])
                                            EPC.append(entry['prom9'])
                                            CEPC.append(entry['conta9'])
                                            postgrado.append(entry['prom10'])
                                            Cpostgrado.append(entry['conta10'])
                                            nosabe.append(entry['prom11'])
                                            Cnosabe.append(entry['conta11'])


            else:
                if (inst == "General"):
                    if (categoria == "Genero"):

                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'])
                            femenino.append(entry['prom1'])
                            masculino.append(entry['prom2'])
                            Cfemenino.append(entry['conta1'])
                            Cmasculino.append(entry['conta2'])
                    else:
                        if (categoria == "Condicion de las TIC"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                                conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                                conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                                'id_institucion__cole_nombre_sede')
                            for entry in result:
                                label.append(
                                    entry['id_institucion__cole_nombre_sede'])
                                ticbuena.append(entry['prom1'])
                                Cticbuena.append(entry['conta1'])
                                ticregular.append(entry['prom2'])
                                Cticregular.append(entry['conta2'])
                                ticmala.append(entry['prom3'])
                                Cticmala.append(entry['conta3'])

                        else:
                            if (categoria == "Condicion de la vivienda"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje,
                                              filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                                    prom2=Round(Avg(puntaje,
                                              filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                                    conta1=Count('id_estudiante',
                                                 filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                    conta2=Count('id_estudiante',
                                                 filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                    conta3=Count('id_estudiante',
                                                 filter=Q(
                                                     id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                    id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                                    'id_institucion__cole_nombre_sede')
                                for entry in result:
                                    label.append(
                                        entry['id_institucion__cole_nombre_sede'])
                                    Hmedio.append(entry['prom1'])
                                    CHmedio.append(entry['conta1'])
                                    Hcritico.append(entry['prom2'])
                                    CHcritico.append(entry['conta2'])
                                    Hsin.append(entry['prom3'])
                                    CHsin.append(entry['conta3'])

                            else:
                                if (categoria == "Rango de Edad"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                                        'id_tiempo__ano', 'id_institucion__cole_nombre_sede')
                                    for entry in result:
                                        label.append(
                                            entry['id_institucion__cole_nombre_sede'])
                                        e17.append(entry['prom1'])
                                        Ce17.append(entry['conta1'])
                                        e18y19.append(entry['prom2'])
                                        Ce18y19.append(entry['conta2'])
                                        e20a28.append(entry['prom3'])
                                        Ce20a28.append(entry['conta3'])
                                        emayoresde28.append(entry['prom4'])
                                        Cemayoresde28.append(entry['conta4'])
                                        emenoresde17.append(entry['prom5'])
                                        Cemenoresde17.append(entry['conta5'])

                                else:
                                    if (categoria == "Estrato"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
                                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                            prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                            prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                            prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                            conta1=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                            conta2=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                            conta3=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                            conta4=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                            conta5=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                            conta6=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="6"))).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                                            'id_institucion__cole_nombre_sede')
                                        for entry in result:
                                            label.append(
                                                entry['id_institucion__cole_nombre_sede'])
                                            es1.append(entry['prom1'])
                                            Ces1.append(entry['conta1'])
                                            es2.append(entry['prom2'])
                                            Ces2.append(entry['conta2'])
                                            es3.append(entry['prom3'])
                                            Ces3.append(entry['conta3'])
                                            es4.append(entry['prom4'])
                                            Ces4.append(entry['conta4'])
                                            es5.append(entry['prom5'])
                                            Ces5.append(entry['conta5'])
                                            es6.append(entry['prom6'])
                                            Ces6.append(entry['conta6'])
                                    else:
                                        if (categoria == "Nivel Educativo Padres"):
                                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                                'id_tiempo__ano').annotate(
                                                prom1=Round(Avg(puntaje,
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                                prom2=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                                prom3=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                                prom4=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                                prom5=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                                prom6=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                                prom7=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                                prom8=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                                prom9=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                                prom10=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                                prom11=Round(Avg(puntaje,
                                                           filter=Q(
                                                               id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                                conta1=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                                conta2=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                                conta3=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                                conta4=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                                conta5=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                                conta6=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                                conta7=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                                conta8=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                                conta9=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                                conta10=Count('id_estudiante',
                                                              filter=Q(
                                                                  id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                                conta11=Count('id_estudiante',
                                                              filter=Q(
                                                                  id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                            ).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                                                'id_institucion__cole_nombre_sede')
                                            for entry in result:
                                                label.append(
                                                    entry['id_institucion__cole_nombre_sede'])
                                                n.append(entry['prom1'])
                                                Cn.append(entry['conta1'])
                                                PI.append(entry['prom2'])
                                                CPI.append(entry['conta2'])
                                                PC.append(entry['prom3'])
                                                CPC.append(entry['conta3'])
                                                BI.append(entry['prom4'])
                                                CBI.append(entry['conta4'])
                                                BC.append(entry['prom5'])
                                                CBC.append(entry['conta5'])
                                                ETI.append(entry['prom6'])
                                                CETI.append(entry['conta6'])
                                                ETC.append(entry['prom7'])
                                                CETC.append(entry['conta7'])
                                                EPI.append(entry['prom8'])
                                                CEPI.append(entry['conta8'])
                                                EPC.append(entry['prom9'])
                                                CEPC.append(entry['conta9'])
                                                postgrado.append(entry['prom10'])
                                                Cpostgrado.append(entry['conta10'])
                                                nosabe.append(entry['prom11'])
                                                Cnosabe.append(entry['conta11'])
                else:
                    if (categoria == "Genero"):

                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO"))),
                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO"))),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'])
                            femenino.append(entry['prom1'])
                            masculino.append(entry['prom2'])
                            Cfemenino.append(entry['conta1'])
                            Cmasculino.append(entry['conta2'])
                    else:
                        if (categoria == "Condicion de las TIC"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
                                prom1=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA"))),
                                prom2=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR"))),
                                prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA"))),
                                conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                                conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                                'id_institucion__cole_nombre_sede')
                            for entry in result:
                                label.append(
                                    entry['id_institucion__cole_nombre_sede'])
                                ticbuena.append(entry['prom1'])
                                Cticbuena.append(entry['conta1'])
                                ticregular.append(entry['prom2'])
                                Cticregular.append(entry['conta2'])
                                ticmala.append(entry['prom3'])
                                Cticmala.append(entry['conta3'])

                        else:
                            if (categoria == "Condicion en la que vive"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
                                    prom1=Round(Avg(puntaje,
                                              filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO"))),
                                    prom2=Round(Avg(puntaje,
                                              filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO"))),
                                    prom3=Round(Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))),
                                    conta1=Count('id_estudiante',
                                                 filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                    conta2=Count('id_estudiante',
                                                 filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                    conta3=Count('id_estudiante',
                                                 filter=Q(
                                                     id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                    id_lugar__cole_mcpio_ubicacion=message,
                                    id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                                    'id_institucion__cole_nombre_sede')
                                for entry in result:
                                    label.append(
                                        entry['id_institucion__cole_nombre_sede'])
                                    Hmedio.append(entry['prom1'])
                                    CHmedio.append(entry['conta1'])
                                    Hcritico.append(entry['prom2'])
                                    CHcritico.append(entry['conta2'])
                                    Hsin.append(entry['prom3'])
                                    CHsin.append(entry['conta3'])

                            else:
                                if (categoria == "Rango de Edad"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
                                        prom1=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="17"))),
                                        prom2=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="18 Y 19"))),
                                        prom3=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="20 A 28"))),
                                        prom4=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28"))),
                                        prom5=Round(Avg(puntaje, filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))),
                                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                        conta2=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                        conta3=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                        conta4=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                        conta5=Count('id_estudiante',
                                                     filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                                        'id_tiempo__ano', 'id_institucion__cole_nombre_sede')
                                    for entry in result:
                                        label.append(
                                            entry['id_institucion__cole_nombre_sede'])
                                        e17.append(entry['prom1'])
                                        Ce17.append(entry['conta1'])
                                        e18y19.append(entry['prom2'])
                                        Ce18y19.append(entry['conta2'])
                                        e20a28.append(entry['prom3'])
                                        Ce20a28.append(entry['conta3'])
                                        emayoresde28.append(entry['prom4'])
                                        Cemayoresde28.append(entry['conta4'])
                                        emenoresde17.append(entry['prom5'])
                                        Cemenoresde17.append(entry['conta5'])

                                else:
                                    if (categoria == "Estrato"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
                                            prom1=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="1"))),
                                            prom2=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="2"))),
                                            prom3=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="3"))),
                                            prom4=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="4"))),
                                            prom5=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="5"))),
                                            prom6=Round(Avg(puntaje, filter=Q(id_estudiante__fami_estrato_vivienda="6"))),
                                            conta1=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                            conta2=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                            conta3=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                            conta4=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                            conta5=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                            conta6=Count('id_estudiante',
                                                         filter=Q(id_estudiante__fami_estrato_vivienda="6"))).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                                            'id_institucion__cole_nombre_sede')
                                        for entry in result:
                                            label.append(
                                                entry['id_institucion__cole_nombre_sede'])
                                            es1.append(entry['prom1'])
                                            Ces1.append(entry['conta1'])
                                            es2.append(entry['prom2'])
                                            Ces2.append(entry['conta2'])
                                            es3.append(entry['prom3'])
                                            Ces3.append(entry['conta3'])
                                            es4.append(entry['prom4'])
                                            Ces4.append(entry['conta4'])
                                            es5.append(entry['prom5'])
                                            Ces5.append(entry['conta5'])
                                            es6.append(entry['prom6'])
                                            Ces6.append(entry['conta6'])
                                    else:
                                        if (categoria == "Nivel Educativo Padres"):
                                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                                'id_tiempo__ano').annotate(
                                                prom1=Round(Avg(puntaje,
                                                          filter=Q(
                                                              id_estudiante__fami_max_nivel_educa_padres="NINGUNO"))),
                                                prom2=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA"))),
                                                prom3=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA"))),
                                                prom4=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO"))),
                                                prom5=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO"))),
                                                prom6=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA"))),
                                                prom7=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA"))),
                                                prom8=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                                prom9=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA"))),
                                                prom10=Round(Avg(puntaje, filter=Q(
                                                    id_estudiante__fami_max_nivel_educa_padres="POSTGRADO"))),
                                                prom11=Round(Avg(puntaje,
                                                           filter=Q(
                                                               id_estudiante__fami_max_nivel_educa_padres="NO SABE"))),
                                                conta1=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
                                                conta2=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")),
                                                conta3=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")),
                                                conta4=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")),
                                                conta5=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")),
                                                conta6=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")),
                                                conta7=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")),
                                                conta8=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                                conta9=Count('id_estudiante',
                                                             filter=Q(
                                                                 id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")),
                                                conta10=Count('id_estudiante',
                                                              filter=Q(
                                                                  id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                                conta11=Count('id_estudiante',
                                                              filter=Q(
                                                                  id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                            ).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano).order_by(
                                                'id_institucion__cole_nombre_sede')
                                            for entry in result:
                                                label.append(
                                                    entry['id_institucion__cole_nombre_sede'])
                                                n.append(entry['prom1'])
                                                Cn.append(entry['conta1'])
                                                PI.append(entry['prom2'])
                                                CPI.append(entry['conta2'])
                                                PC.append(entry['prom3'])
                                                CPC.append(entry['conta3'])
                                                BI.append(entry['prom4'])
                                                CBI.append(entry['conta4'])
                                                BC.append(entry['prom5'])
                                                CBC.append(entry['conta5'])
                                                ETI.append(entry['prom6'])
                                                CETI.append(entry['conta6'])
                                                ETC.append(entry['prom7'])
                                                CETC.append(entry['conta7'])
                                                EPI.append(entry['prom8'])
                                                CEPI.append(entry['conta8'])
                                                EPC.append(entry['prom9'])
                                                CEPC.append(entry['conta9'])
                                                postgrado.append(entry['prom10'])
                                                Cpostgrado.append(entry['conta10'])
                                                nosabe.append(entry['prom11'])
                                                Cnosabe.append(entry['conta11'])


    # masculino = np.around(masculino)
    return JsonResponse(data={

        'labels': label,
        'data': dato,
        'conta': contador,
        'categoria': categoria1,
        'con': contad,
        'masculino': masculino,
        'Cmasculino': Cmasculino,
        'femenino': femenino,
        'Cfemenino': Cfemenino,
        'ticbuena': ticbuena,
        'ticregular': ticregular,
        'ticmala': ticmala,
        'Hmedio': Hmedio,
        'Hcritico': Hcritico,
        'Hsin': Hsin,
        'e17': e17,
        'e18y19': e18y19,
        'e20a28': e20a28,
        'emayoresde28': emayoresde28,
        'emenoresde17': emenoresde17,
        'es1': es1,
        'es2': es2,
        'es3': es3,
        'es4': es4,
        'es5': es5,
        'es6': es6,
        'EPC': EPC,
        'EPI': EPI,
        'ETC': ETC,
        'ETI': ETI,
        'n': n,
        'nosabe': nosabe,
        'postgrado': postgrado,
        'PC': PC,
        'PI': PI,
        'BC': BC,
        'BI': BI,
        'Cticbuena': Cticbuena,
        'Cticregular': Cticregular,
        'Cticmala': Cticmala,
        'CHmedio': CHmedio,
        'CHcritico': CHcritico,
        'CHsin': CHsin,
        'Ce17': Ce17,
        'Ce18y19': Ce18y19,
        'Ce20a28': Ce20a28,
        'Cemayoresde28': Cemayoresde28,
        'Cemenoresde17': Cemenoresde17,
        'Ces1': Ces1,
        'Ces2': Ces2,
        'Ces3': Ces3,
        'Ces4': Ces4,
        'Ces5': Ces5,
        'Ces6': Ces6,
        'CEPC': CEPC,
        'CEPI': CEPI,
        'CETC': CETC,
        'CETI': CETI,
        'Cn': Cn,
        'Cnosabe': Cnosabe,
        'Cpostgrado': Cpostgrado,
        'CPC': CPC,
        'CPI': CPI,
        'CBC': CBC,
        'CBI': CBI,
    })