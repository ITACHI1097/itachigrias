import cgi
import codecs
import csv
import pandas as pd

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
from django.db.models import Avg, Count, Sum, Q
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
    vivbuena = []
    Cvivbuena = []
    vivregular = []
    Cvivregular = []
    vivmala = []
    Cvivmala = []
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
                    prom1=Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO")),
                    prom2=Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO")),
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
                        prom1=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                        prom2=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                        prom3=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_tic="MALA")),
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
                    if(categoria=="Condicion de la vivienda"):
                        # result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                        #     prom=Avg(puntaje),
                        #     conta=Count(
                        #         'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="BUENA")
                        #
                        # for entry in result:
                        #     label.append(
                        #         entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                        #     dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                        #     vivbuena.append(entry['prom'])
                        #     Cvivbuena.append(entry['conta'])
                        # result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                        #     prom=Avg(puntaje),
                        #     conta=Count(
                        #         'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="REGULAR")
                        #
                        # for entry in result2:
                        #     vivregular.append(entry['prom'])
                        #     Cvivregular.append(entry['conta'])
                        #
                        # result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                        #     prom=Avg(puntaje),
                        #     conta=Count(
                        #         'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="MALA")
                        #
                        # for entry in result3:
                        #     vivmala.append(entry['prom'])
                        #     Cvivmala.append(entry['conta'])

                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                            'id_tiempo__ano').annotate(
                            prom1=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vivienda="BUENA")),
                            prom2=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vivienda="REGULAR")),
                            prom3=Avg(puntaje, filter=Q(id_estudiante__eco_condicion_vivienda="MALA")),
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vivienda="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vivienda="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_vivienda="MALA"))).order_by(
                            'id_lugar__cole_mcpio_ubicacion')
                        for entry in result:
                            label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                            vivbuena.append(entry['prom1'])
                            Cvivbuena.append(entry['conta1'])
                            vivregular.append(entry['prom2'])
                            Cvivregular.append(entry['conta2'])
                            vivmala.append(entry['prom3'])
                            Cvivmala.append(entry['conta3'])

                    else:
                        if(categoria=="Rango de Edad"):
                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__estu_rango_edad="17")

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                                e17.append(entry['prom'])
                                Ce17.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__estu_rango_edad="18 Y 19")

                            for entry in result2:
                                e18y19.append(entry['prom'])
                                Ce18y19.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__estu_rango_edad="20 A 28")

                            for entry in result3:
                                e20a28.append(entry['prom'])
                                Ce20a28.append(entry['conta'])

                            result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__estu_rango_edad="MAYORES DE 28")

                            for entry in result4:
                                emayoresde28.append(entry['prom'])
                                Cemayoresde28.append(entry['conta'])

                            result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__estu_rango_edad="MENORES DE 17")

                            for entry in result5:
                                emenoresde17.append(entry['prom'])
                                Cemenoresde17.append(entry['conta'])

                        else:
                            if(categoria=="Estrato"):
                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="1")

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_lugar__cole_mcpio_ubicacion'])
                                    es1.append(entry['prom'])
                                    Ces1.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="2")

                                for entry in result2:
                                    es2.append(entry['prom'])
                                    Ces2.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="3")

                                for entry in result3:
                                    es3.append(entry['prom'])
                                    Ces3.append(entry['conta'])

                                result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="4")

                                for entry in result4:
                                    es4.append(entry['prom'])
                                    Ces4.append(entry['conta'])

                                result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="5")

                                for entry in result5:
                                    es5.append(entry['prom'])
                                    Ces5.append(entry['conta'])

                                result6 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="6")

                                for entry in result6:
                                    es6.append(entry['prom'])
                                    Ces6.append(entry['conta'])
                            else:
                                if(categoria == "Nivel Educativo Padres"):
                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="NINGUNO")

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                                        n.append(entry['prom'])
                                        Cn.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")

                                    for entry in result2:
                                        PI.append(entry['prom'])
                                        CPI.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")

                                    for entry in result3:
                                        PC.append(entry['prom'])
                                        CPC.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")

                                    for entry in result4:
                                        BI.append(entry['prom'])
                                        CBI.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")

                                    for entry in result5:
                                        BC.append(entry['prom'])
                                        CBC.append(entry['conta'])

                                    result6 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")

                                    for entry in result6:
                                        ETI.append(entry['prom'])
                                        CETI.append(entry['conta'])

                                    result7 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")

                                    for entry in result7:
                                        ETC.append(entry['prom'])
                                        CETC.append(entry['conta'])

                                    result8 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")

                                    for entry in result8:
                                        EPI.append(entry['prom'])
                                        CEPI.append(entry['conta'])

                                    result9 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA")

                                    for entry in result9:
                                        EPC.append(entry['prom'])
                                        CEPC.append(entry['conta'])

                                    result10 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")

                                    for entry in result10:
                                        postgrado.append(entry['prom'])
                                        Cpostgrado.append(entry['conta'])

                                    result11 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_estudiante__fami_max_nivel_educa_padres="NO SABE")

                                    for entry in result11:
                                        nosabe.append(entry['prom'])
                                        Cnosabe.append(entry['conta'])

        else:
            if (inst == "General"):
                if (categoria == "Genero"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede','id_tiempo__ano').annotate(prom1=Avg(puntaje, filter=Q(id_estudiante__estu_genero="MASCULINO")),prom2=Avg(puntaje, filter=Q(id_estudiante__estu_genero="FEMENINO")),conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(id_lugar__cole_mcpio_ubicacion=message).order_by('id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede']+" : "+entry['id_tiempo__ano'])
                        femenino.append(entry['prom1'])
                        masculino.append(entry['prom2'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])

                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_tic="BUENA")

                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            ticbuena.append(entry['prom'])
                            Cticbuena.append(entry['conta'])
                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_tic="REGULAR")

                        for entry in result2:
                            ticregular.append(entry['prom'])
                            Cticregular.append(entry['conta'])

                        result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_tic="MALA")

                        for entry in result3:
                            ticmala.append(entry['prom'])
                            Cticmala.append(entry['conta'])

                    else:
                        if (categoria == "Condicion de la vivienda"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_vivienda="BUENA")

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_institucion__cole_nombre_sede'])
                                vivbuena.append(entry['prom'])
                                Cvivbuena.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_vivienda="REGULAR")

                            for entry in result2:
                                vivregular.append(entry['prom'])
                                Cvivregular.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__eco_condicion_vivienda="MALA")

                            for entry in result3:
                                vivmala.append(entry['prom'])
                                Cvivmala.append(entry['conta'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__estu_rango_edad="17")

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_institucion__cole_nombre_sede'])
                                    e17.append(entry['prom'])
                                    Ce17.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__estu_rango_edad="18 Y 19")

                                for entry in result2:
                                    e18y19.append(entry['prom'])
                                    Ce18y19.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__estu_rango_edad="20 A 28")

                                for entry in result3:
                                    e20a28.append(entry['prom'])
                                    Ce20a28.append(entry['conta'])

                                result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__estu_rango_edad="MAYORES DE 28")

                                for entry in result4:
                                    emayoresde28.append(entry['prom'])
                                    Cemayoresde28.append(entry['conta'])

                                result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__estu_rango_edad="MENORES DE 17")

                                for entry in result5:
                                    emenoresde17.append(entry['prom'])
                                    Cemenoresde17.append(entry['conta'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="1")

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_institucion__cole_nombre_sede'])
                                        es1.append(entry['prom'])
                                        Ces1.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="2")

                                    for entry in result2:
                                        es2.append(entry['prom'])
                                        Ces2.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="3")

                                    for entry in result3:
                                        es3.append(entry['prom'])
                                        Ces3.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="4")

                                    for entry in result4:
                                        es4.append(entry['prom'])
                                        Ces4.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="5")

                                    for entry in result5:
                                        es5.append(entry['prom'])
                                        Ces5.append(entry['conta'])

                                    result6 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_estrato_vivienda="6")

                                    for entry in result6:
                                        es6.append(entry['prom'])
                                        Ces6.append(entry['conta'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_estudiante__fami_max_nivel_educa_padres="NINGUNO")

                                        for entry in result:
                                            label.append(
                                                entry[
                                                    'id_institucion__cole_nombre_sede'])
                                            n.append(entry['prom'])
                                            Cn.append(entry['conta'])
                                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")

                                        for entry in result2:
                                            PI.append(entry['prom'])
                                            CPI.append(entry['conta'])

                                        result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")

                                        for entry in result3:
                                            PC.append(entry['prom'])
                                            CPC.append(entry['conta'])

                                        result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")

                                        for entry in result4:
                                            BI.append(entry['prom'])
                                            CBI.append(entry['conta'])

                                        result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")

                                        for entry in result5:
                                            BC.append(entry['prom'])
                                            CBC.append(entry['conta'])

                                        result6 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")

                                        for entry in result6:
                                            ETI.append(entry['prom'])
                                            CETI.append(entry['conta'])

                                        result7 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")

                                        for entry in result7:
                                            ETC.append(entry['prom'])
                                            CETC.append(entry['conta'])

                                        result8 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")

                                        for entry in result8:
                                            EPI.append(entry['prom'])
                                            CEPI.append(entry['conta'])

                                        result9 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA")

                                        for entry in result9:
                                            EPC.append(entry['prom'])
                                            CEPC.append(entry['conta'])

                                        result10 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")

                                        for entry in result10:
                                            postgrado.append(entry['prom'])
                                            Cpostgrado.append(entry['conta'])

                                        result11 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message,
                                            id_estudiante__fami_max_nivel_educa_padres="NO SABE")

                                        for entry in result11:
                                            nosabe.append(entry['prom'])
                                            Cnosabe.append(entry['conta'])
            else:
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                     conta=Count(
                                                                                                         'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_genero="MASCULINO")

                    for entry in result:
                        label.append(
                            entry['id_institucion__cole_nombre_sede'])
                        masculino.append(entry['prom'])
                        Cmasculino.append(entry['conta'])
                    result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Avg(puntaje),
                                                                                                    conta=Count(
                                                                                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_genero="FEMENINO")
                    for entry in result2:
                        femenino.append(entry['prom'])
                        Cfemenino.append(entry['conta'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_tic="BUENA")

                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            ticbuena.append(entry['prom'])
                            Cticbuena.append(entry['conta'])
                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_tic="REGULAR")

                        for entry in result2:
                            ticregular.append(entry['prom'])
                            Cticregular.append(entry['conta'])

                        result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_tic="MALA")

                        for entry in result3:
                            ticmala.append(entry['prom'])
                            Cticmala.append(entry['conta'])

                    else:
                        if (categoria == "Condicion de la vivienda"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_vivienda="BUENA")

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_institucion__cole_nombre_sede'])
                                vivbuena.append(entry['prom'])
                                Cvivbuena.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_vivienda="REGULAR")

                            for entry in result2:
                                vivregular.append(entry['prom'])
                                Cvivregular.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__eco_condicion_vivienda="MALA")

                            for entry in result3:
                                vivmala.append(entry['prom'])
                                Cvivmala.append(entry['conta'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_rango_edad="17")

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_institucion__cole_nombre_sede'])
                                    e17.append(entry['prom'])
                                    Ce17.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_rango_edad="18 Y 19")

                                for entry in result2:
                                    e18y19.append(entry['prom'])
                                    Ce18y19.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_rango_edad="20 A 28")

                                for entry in result3:
                                    e20a28.append(entry['prom'])
                                    Ce20a28.append(entry['conta'])

                                result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_rango_edad="MAYORES DE 28")

                                for entry in result4:
                                    emayoresde28.append(entry['prom'])
                                    Cemayoresde28.append(entry['conta'])

                                result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__estu_rango_edad="MENORES DE 17")

                                for entry in result5:
                                    emenoresde17.append(entry['prom'])
                                    Cemenoresde17.append(entry['conta'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="1")

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_institucion__cole_nombre_sede'])
                                        es1.append(entry['prom'])
                                        Ces1.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="2")

                                    for entry in result2:
                                        es2.append(entry['prom'])
                                        Ces2.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="3")

                                    for entry in result3:
                                        es3.append(entry['prom'])
                                        Ces3.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="4")

                                    for entry in result4:
                                        es4.append(entry['prom'])
                                        Ces4.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="5")

                                    for entry in result5:
                                        es5.append(entry['prom'])
                                        Ces5.append(entry['conta'])

                                    result6 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_estrato_vivienda="6")

                                    for entry in result6:
                                        es6.append(entry['prom'])
                                        Ces6.append(entry['conta'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_estudiante__fami_max_nivel_educa_padres="NINGUNO")

                                        for entry in result:
                                            label.append(
                                                entry[
                                                    'id_institucion__cole_nombre_sede'])
                                            n.append(entry['prom'])
                                            Cn.append(entry['conta'])
                                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")

                                        for entry in result2:
                                            PI.append(entry['prom'])
                                            CPI.append(entry['conta'])

                                        result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")

                                        for entry in result3:
                                            PC.append(entry['prom'])
                                            CPC.append(entry['conta'])

                                        result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")

                                        for entry in result4:
                                            BI.append(entry['prom'])
                                            CBI.append(entry['conta'])

                                        result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")

                                        for entry in result5:
                                            BC.append(entry['prom'])
                                            CBC.append(entry['conta'])

                                        result6 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")

                                        for entry in result6:
                                            ETI.append(entry['prom'])
                                            CETI.append(entry['conta'])

                                        result7 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")

                                        for entry in result7:
                                            ETC.append(entry['prom'])
                                            CETC.append(entry['conta'])

                                        result8 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")

                                        for entry in result8:
                                            EPI.append(entry['prom'])
                                            CEPI.append(entry['conta'])

                                        result9 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA")

                                        for entry in result9:
                                            EPC.append(entry['prom'])
                                            CEPC.append(entry['conta'])

                                        result10 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")

                                        for entry in result10:
                                            postgrado.append(entry['prom'])
                                            Cpostgrado.append(entry['conta'])

                                        result11 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                                            id_estudiante__fami_max_nivel_educa_padres="NO SABE")

                                        for entry in result11:
                                            nosabe.append(entry['prom'])
                                            Cnosabe.append(entry['conta'])


    else:
            if (message == "TODOS"):
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg(puntaje),
                                                                                                   conta=Count(
                                                                                                       'id_estudiante')).filter(id_estudiante__estu_genero="MASCULINO", id_tiempo__ano=ano)

                    for entry in result:
                        label.append(
                            entry['id_lugar__cole_mcpio_ubicacion'])
                        masculino.append(entry['prom'])
                        Cmasculino.append(entry['conta'])
                    result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Avg(puntaje),
                                                                                                    conta=Count(
                                                                                                        'id_estudiante')).filter(id_estudiante__estu_genero="FEMENINO", id_tiempo__ano=ano)
                    for entry in result2:
                        femenino.append(entry['prom'])
                        Cfemenino.append(entry['conta'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(id_estudiante__eco_condicion_tic="BUENA", id_tiempo__ano=ano)

                        for entry in result:
                            label.append(
                                entry['id_lugar__cole_mcpio_ubicacion'])
                            ticbuena.append(entry['prom'])
                            Cticbuena.append(entry['conta'])
                        result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(id_estudiante__eco_condicion_tic="REGULAR", id_tiempo__ano=ano)

                        for entry in result2:
                            ticregular.append(entry['prom'])
                            Cticregular.append(entry['conta'])

                        result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(id_estudiante__eco_condicion_tic="MALA", id_tiempo__ano=ano)

                        for entry in result3:
                            ticmala.append(entry['prom'])
                            Cticmala.append(entry['conta'])

                    else:
                        if (categoria == "Condicion de la vivienda"):
                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="BUENA", id_tiempo__ano=ano)

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_lugar__cole_mcpio_ubicacion'])
                                vivbuena.append(entry['prom'])
                                Cvivbuena.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="REGULAR", id_tiempo__ano=ano)

                            for entry in result2:
                                vivregular.append(entry['prom'])
                                Cvivregular.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(id_estudiante__eco_condicion_vivienda="MALA", id_tiempo__ano=ano)

                            for entry in result3:
                                vivmala.append(entry['prom'])
                                Cvivmala.append(entry['conta'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__estu_rango_edad="17", id_tiempo__ano=ano)

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_lugar__cole_mcpio_ubicacion'])
                                    e17.append(entry['prom'])
                                    Ce17.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__estu_rango_edad="18 Y 19", id_tiempo__ano=ano)

                                for entry in result2:
                                    e18y19.append(entry['prom'])
                                    Ce18y19.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__estu_rango_edad="20 A 28", id_tiempo__ano=ano)

                                for entry in result3:
                                    e20a28.append(entry['prom'])
                                    Ce20a28.append(entry['conta'])

                                result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__estu_rango_edad="MAYORES DE 28", id_tiempo__ano=ano)

                                for entry in result4:
                                    emayoresde28.append(entry['prom'])
                                    Cemayoresde28.append(entry['conta'])

                                result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(id_estudiante__estu_rango_edad="MENORES DE 17", id_tiempo__ano=ano)

                                for entry in result5:
                                    emenoresde17.append(entry['prom'])
                                    Cemenoresde17.append(entry['conta'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="1", id_tiempo__ano=ano)

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_lugar__cole_mcpio_ubicacion'])
                                        es1.append(entry['prom'])
                                        Ces1.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="2", id_tiempo__ano=ano)

                                    for entry in result2:
                                        es2.append(entry['prom'])
                                        Ces2.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="3", id_tiempo__ano=ano)

                                    for entry in result3:
                                        es3.append(entry['prom'])
                                        Ces3.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="4", id_tiempo__ano=ano)

                                    for entry in result4:
                                        es4.append(entry['prom'])
                                        Ces4.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="5", id_tiempo__ano=ano)

                                    for entry in result5:
                                        es5.append(entry['prom'])
                                        Ces5.append(entry['conta'])

                                    result6 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(id_estudiante__fami_estrato_vivienda="6", id_tiempo__ano=ano)

                                    for entry in result6:
                                        es6.append(entry['prom'])
                                        Ces6.append(entry['conta'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(id_estudiante__fami_max_nivel_educa_padres="NINGUNO", id_tiempo__ano=ano)

                                        for entry in result:
                                            label.append(
                                                entry[
                                                    'id_lugar__cole_mcpio_ubicacion'])
                                            n.append(entry['prom'])
                                            Cn.append(entry['conta'])
                                        result2 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA", id_tiempo__ano=ano)

                                        for entry in result2:
                                            PI.append(entry['prom'])
                                            CPI.append(entry['conta'])

                                        result3 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA", id_tiempo__ano=ano)

                                        for entry in result3:
                                            PC.append(entry['prom'])
                                            CPC.append(entry['conta'])

                                        result4 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO", id_tiempo__ano=ano)

                                        for entry in result4:
                                            BI.append(entry['prom'])
                                            CBI.append(entry['conta'])

                                        result5 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO", id_tiempo__ano=ano)

                                        for entry in result5:
                                            BC.append(entry['prom'])
                                            CBC.append(entry['conta'])

                                        result6 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA", id_tiempo__ano=ano)

                                        for entry in result6:
                                            ETI.append(entry['prom'])
                                            CETI.append(entry['conta'])

                                        result7 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA", id_tiempo__ano=ano)

                                        for entry in result7:
                                            ETC.append(entry['prom'])
                                            CETC.append(entry['conta'])

                                        result8 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA", id_tiempo__ano=ano)

                                        for entry in result8:
                                            EPI.append(entry['prom'])
                                            CEPI.append(entry['conta'])

                                        result9 = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA", id_tiempo__ano=ano)

                                        for entry in result9:
                                            EPC.append(entry['prom'])
                                            CEPC.append(entry['conta'])

                                        result10 = FactSaber11.objects.values(
                                            'id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="POSTGRADO", id_tiempo__ano=ano)

                                        for entry in result10:
                                            postgrado.append(entry['prom'])
                                            Cpostgrado.append(entry['conta'])

                                        result11 = FactSaber11.objects.values(
                                            'id_lugar__cole_mcpio_ubicacion').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_estudiante__fami_max_nivel_educa_padres="NO SABE", id_tiempo__ano=ano)

                                        for entry in result11:
                                            nosabe.append(entry['prom'])
                                            Cnosabe.append(entry['conta'])


            else:
                if (inst == "General"):
                    if (categoria == "Genero"):

                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_genero="MASCULINO")

                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            masculino.append(entry['prom'])
                            Cmasculino.append(entry['conta'])
                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_genero="FEMENINO")
                        for entry in result2:
                            femenino.append(entry['prom'])
                            Cfemenino.append(entry['conta'])
                    else:
                        if (categoria == "Condicion de las TIC"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="BUENA")

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_institucion__cole_nombre_sede'])
                                ticbuena.append(entry['prom'])
                                Cticbuena.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="REGULAR")

                            for entry in result2:
                                ticregular.append(entry['prom'])
                                Cticregular.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="MALA")

                            for entry in result3:
                                ticmala.append(entry['prom'])
                                Cticmala.append(entry['conta'])

                        else:
                            if (categoria == "Condicion de la vivienda"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="BUENA")

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_institucion__cole_nombre_sede'])
                                    vivbuena.append(entry['prom'])
                                    Cvivbuena.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="REGULAR")

                                for entry in result2:
                                    vivregular.append(entry['prom'])
                                    Cvivregular.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="MALA")

                                for entry in result3:
                                    vivmala.append(entry['prom'])
                                    Cvivmala.append(entry['conta'])

                            else:
                                if (categoria == "Rango de Edad"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="17")

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_institucion__cole_nombre_sede'])
                                        e17.append(entry['prom'])
                                        Ce17.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="18 Y 19")

                                    for entry in result2:
                                        e18y19.append(entry['prom'])
                                        Ce18y19.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="20 A 28")

                                    for entry in result3:
                                        e20a28.append(entry['prom'])
                                        Ce20a28.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="MAYORES DE 28")

                                    for entry in result4:
                                        emayoresde28.append(entry['prom'])
                                        Cemayoresde28.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="MENORES DE 17")

                                    for entry in result5:
                                        emenoresde17.append(entry['prom'])
                                        Cemenoresde17.append(entry['conta'])

                                else:
                                    if (categoria == "Estrato"):
                                        result = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="1")

                                        for entry in result:
                                            label.append(
                                                entry[
                                                    'id_institucion__cole_nombre_sede'])
                                            es1.append(entry['prom'])
                                            Ces1.append(entry['conta'])
                                        result2 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="2")

                                        for entry in result2:
                                            es2.append(entry['prom'])
                                            Ces2.append(entry['conta'])

                                        result3 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="3")

                                        for entry in result3:
                                            es3.append(entry['prom'])
                                            Ces3.append(entry['conta'])

                                        result4 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="4")

                                        for entry in result4:
                                            es4.append(entry['prom'])
                                            Ces4.append(entry['conta'])

                                        result5 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="5")

                                        for entry in result5:
                                            es5.append(entry['prom'])
                                            Ces5.append(entry['conta'])

                                        result6 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="6")

                                        for entry in result6:
                                            es6.append(entry['prom'])
                                            Ces6.append(entry['conta'])
                                    else:
                                        if (categoria == "Nivel Educativo Padres"):
                                            result = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano, id_estudiante__fami_max_nivel_educa_padres="NINGUNO")

                                            for entry in result:
                                                label.append(
                                                    entry[
                                                        'id_institucion__cole_nombre_sede'])
                                                n.append(entry['prom'])
                                                Cn.append(entry['conta'])
                                            result2 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")

                                            for entry in result2:
                                                PI.append(entry['prom'])
                                                CPI.append(entry['conta'])

                                            result3 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")

                                            for entry in result3:
                                                PC.append(entry['prom'])
                                                CPC.append(entry['conta'])

                                            result4 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")

                                            for entry in result4:
                                                BI.append(entry['prom'])
                                                CBI.append(entry['conta'])

                                            result5 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")

                                            for entry in result5:
                                                BC.append(entry['prom'])
                                                CBC.append(entry['conta'])

                                            result6 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")

                                            for entry in result6:
                                                ETI.append(entry['prom'])
                                                CETI.append(entry['conta'])

                                            result7 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")

                                            for entry in result7:
                                                ETC.append(entry['prom'])
                                                CETC.append(entry['conta'])

                                            result8 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")

                                            for entry in result8:
                                                EPI.append(entry['prom'])
                                                CEPI.append(entry['conta'])

                                            result9 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA")

                                            for entry in result9:
                                                EPC.append(entry['prom'])
                                                CEPC.append(entry['conta'])

                                            result10 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")

                                            for entry in result10:
                                                postgrado.append(entry['prom'])
                                                Cpostgrado.append(entry['conta'])

                                            result11 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="NO SABE")

                                            for entry in result11:
                                                nosabe.append(entry['prom'])
                                                Cnosabe.append(entry['conta'])
                else:
                    if (categoria == "Genero"):

                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_genero="MASCULINO")

                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            masculino.append(entry['prom'])
                            Cmasculino.append(entry['conta'])
                        result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                            prom=Avg(puntaje),
                            conta=Count(
                                'id_estudiante')).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_genero="FEMENINO")
                        for entry in result2:
                            femenino.append(entry['prom'])
                            Cfemenino.append(entry['conta'])
                    else:
                        if (categoria == "Condicion de las TIC"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="BUENA")

                            for entry in result:
                                label.append(
                                    entry[
                                        'id_institucion__cole_nombre_sede'])
                                ticbuena.append(entry['prom'])
                                Cticbuena.append(entry['conta'])
                            result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="REGULAR")

                            for entry in result2:
                                ticregular.append(entry['prom'])
                                Cticregular.append(entry['conta'])

                            result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                prom=Avg(puntaje),
                                conta=Count(
                                    'id_estudiante')).filter(
                                id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_tic="MALA")

                            for entry in result3:
                                ticmala.append(entry['prom'])
                                Cticmala.append(entry['conta'])

                        else:
                            if (categoria == "Condicion de la vivienda"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message,
                                    id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="BUENA")

                                for entry in result:
                                    label.append(
                                        entry[
                                            'id_institucion__cole_nombre_sede'])
                                    vivbuena.append(entry['prom'])
                                    Cvivbuena.append(entry['conta'])
                                result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message,
                                    id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="REGULAR")

                                for entry in result2:
                                    vivregular.append(entry['prom'])
                                    Cvivregular.append(entry['conta'])

                                result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                    prom=Avg(puntaje),
                                    conta=Count(
                                        'id_estudiante')).filter(
                                    id_lugar__cole_mcpio_ubicacion=message,
                                    id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__eco_condicion_vivienda="MALA")

                                for entry in result3:
                                    vivmala.append(entry['prom'])
                                    Cvivmala.append(entry['conta'])

                            else:
                                if (categoria == "Rango de Edad"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="17")

                                    for entry in result:
                                        label.append(
                                            entry[
                                                'id_institucion__cole_nombre_sede'])
                                        e17.append(entry['prom'])
                                        Ce17.append(entry['conta'])
                                    result2 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="18 Y 19")

                                    for entry in result2:
                                        e18y19.append(entry['prom'])
                                        Ce18y19.append(entry['conta'])

                                    result3 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="20 A 28")

                                    for entry in result3:
                                        e20a28.append(entry['prom'])
                                        Ce20a28.append(entry['conta'])

                                    result4 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="MAYORES DE 28")

                                    for entry in result4:
                                        emayoresde28.append(entry['prom'])
                                        Cemayoresde28.append(entry['conta'])

                                    result5 = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(
                                        prom=Avg(puntaje),
                                        conta=Count(
                                            'id_estudiante')).filter(
                                        id_lugar__cole_mcpio_ubicacion=message,
                                        id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__estu_rango_edad="MENORES DE 17")

                                    for entry in result5:
                                        emenoresde17.append(entry['prom'])
                                        Cemenoresde17.append(entry['conta'])

                                else:
                                    if (categoria == "Estrato"):
                                        result = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="1")

                                        for entry in result:
                                            label.append(
                                                entry[
                                                    'id_institucion__cole_nombre_sede'])
                                            es1.append(entry['prom'])
                                            Ces1.append(entry['conta'])
                                        result2 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="2")

                                        for entry in result2:
                                            es2.append(entry['prom'])
                                            Ces2.append(entry['conta'])

                                        result3 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="3")

                                        for entry in result3:
                                            es3.append(entry['prom'])
                                            Ces3.append(entry['conta'])

                                        result4 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="4")

                                        for entry in result4:
                                            es4.append(entry['prom'])
                                            Ces4.append(entry['conta'])

                                        result5 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="5")

                                        for entry in result5:
                                            es5.append(entry['prom'])
                                            Ces5.append(entry['conta'])

                                        result6 = FactSaber11.objects.values(
                                            'id_institucion__cole_nombre_sede').annotate(
                                            prom=Avg(puntaje),
                                            conta=Count(
                                                'id_estudiante')).filter(
                                            id_lugar__cole_mcpio_ubicacion=message,
                                            id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano, id_estudiante__fami_estrato_vivienda="6")

                                        for entry in result6:
                                            es6.append(entry['prom'])
                                            Ces6.append(entry['conta'])
                                    else:
                                        if (categoria == "Nivel Educativo Padres"):
                                            result = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_estudiante__fami_max_nivel_educa_padres="NINGUNO", id_tiempo__ano=ano)

                                            for entry in result:
                                                label.append(entry['id_institucion__cole_nombre_sede'])
                                                n.append(entry['prom'])
                                                Cn.append(entry['conta'])
                                            result2 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA INCOMPLETA")

                                            for entry in result2:
                                                PI.append(entry['prom'])
                                                CPI.append(entry['conta'])

                                            result3 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="PRIMARIA COMPLETA")

                                            for entry in result3:
                                                PC.append(entry['prom'])
                                                CPC.append(entry['conta'])

                                            result4 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO IMCOMPLETO")

                                            for entry in result4:
                                                BI.append(entry['prom'])
                                                CBI.append(entry['conta'])

                                            result5 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="SECUNDARIA BACHILLERATO COMPLETO")

                                            for entry in result5:
                                                BC.append(entry['prom'])
                                                CBC.append(entry['conta'])

                                            result6 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA INCOMPLETA")

                                            for entry in result6:
                                                ETI.append(entry['prom'])
                                                CETI.append(entry['conta'])

                                            result7 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION TECNICA O TECNOLOGICA COMPLETA")

                                            for entry in result7:
                                                ETC.append(entry['prom'])
                                                CETC.append(entry['conta'])

                                            result8 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL INCOMPLETA")

                                            for entry in result8:
                                                EPI.append(entry['prom'])
                                                CEPI.append(entry['conta'])

                                            result9 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="EDUCACION PROFECIONAL COMPLETA")

                                            for entry in result9:
                                                EPC.append(entry['prom'])
                                                CEPC.append(entry['conta'])

                                            result10 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")

                                            for entry in result10:
                                                postgrado.append(entry['prom'])
                                                Cpostgrado.append(entry['conta'])

                                            result11 = FactSaber11.objects.values(
                                                'id_institucion__cole_nombre_sede').annotate(
                                                prom=Avg(puntaje),
                                                conta=Count(
                                                    'id_estudiante')).filter(
                                                id_lugar__cole_mcpio_ubicacion=message,
                                                id_institucion__cole_nombre_sede=inst, id_tiempo__ano=ano,
                                                id_estudiante__fami_max_nivel_educa_padres="NO SABE")

                                            for entry in result11:
                                                nosabe.append(entry['prom'])
                                                Cnosabe.append(entry['conta'])


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
        'vivbuena': vivbuena,
        'vivregular': vivregular,
        'vivmala': vivmala,
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
        'Cvivbuena': Cvivbuena,
        'Cvivregular': Cvivregular,
        'Cvivmala': Cvivmala,
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