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