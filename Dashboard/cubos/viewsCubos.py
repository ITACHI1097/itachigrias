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
@allowed_users(allowed_roles=['admin','usuario'])
def generoAno(request):
    label = []
    masculino = []
    femenino = []
    result = FactSaber11.objects.values('id_tiempo__ano').annotate(
        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).order_by(
        'id_tiempo__ano')
    for entry in result:
        label.append(entry['id_tiempo__ano'])
        total = entry['conta1']+entry['conta2']
        masculino.append(round(entry['conta2']/total * 100))
        femenino.append(round(entry['conta1']/total * 100))
    return JsonResponse(data={
        'labels': label,
        'masculino': masculino,
        'femenino': femenino,
    })

def num_mun_ano(request):
    label = []
    punt2012 = []
    punt2013 = []
    punt2014 = []
    punt2015 = []
    punt2016 = []
    punt2017 = []
    punt2018 = []
    punt2019 = []
    punt2020 = []
    punt2021 = []
    punt2022 = []
    punt2023 = []
    # .filter(id_pru_soc_ciu__desemp_soc_ciu='MINIMO')
    satisfactorio = []
    minimo = []
    insuficiente = []
    desmp = []
    cont = []



    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2012' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        label.append(r[0])
        punt2012.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2013' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2013.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2014' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2014.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2015' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2015.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2016' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2016.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2017' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2017.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2018' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2018.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2019' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2019.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2020' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2020.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2021' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2021.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2022' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2022.append(r[1])

    conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select cole_mcpio_ubicacion,count(fact_saber11.id_estudiante) from dim_tiempo,dim_lugares,fact_saber11 where dim_tiempo.id_tiempo=fact_saber11.id_tiempo and dim_lugares.id_lugar=fact_saber11.id_lugar and ano='2023' group by(cole_mcpio_ubicacion,ano) order by(cole_mcpio_ubicacion);"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    for r in row:
        punt2023.append(r[1])


    return JsonResponse(data={
        'labels': label,
        'punt2012': punt2012,
        'punt2013': punt2013,
        'punt2014': punt2014,
        'punt2015': punt2015,
        'punt2016': punt2016,
        'punt2017': punt2017,
        'punt2018': punt2018,
        'punt2019': punt2019,
        'punt2020': punt2020,
        'punt2021': punt2021,
        'punt2022': punt2022,
        'punt2023': punt2023,
    })