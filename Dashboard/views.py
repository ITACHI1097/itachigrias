import cgi
import codecs
import csv
import pandas as pd

from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users
from .forms import FormEntrada
from .models import Entrada
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

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Round(Func):
 function = 'ROUND'
 template='%(function)s(%(expressions)s, 2)'

# Create your views here.
@login_required(login_url='login')
def inicio(request):
    return render(request, "Dashboard/base_0.html")

@unauthenticated_user
def loginPage(request):

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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='admin')
            user.is_staff = True
            user.groups.add(group)


            messages.success(request, 'Registro Exitoso para el Usuario: ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, "Dashboard/register.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def obando(request):
    return render(request, "Dashboard/obando.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def grafic(request):
    return render(request, "Dashboard/grafic.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def subir(request):
    if request.method == 'POST':
         form = FormEntrada(request.POST, request.FILES)
         if form.is_valid():
            insert = Entrada()
            insert.archivo = request.FILES.get('file')
            deli=request.POST.get('delimitador')
            if(insert.archivo == None):
                messages.error(request, "Error, por favor escoja un archivo a subir")
                return render(request, "Dashboard/subir.html")
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
            engine = create_engine('postgresql://postgres:1234@localhost:5432/icfes-1') #revisar para coneccion en amazon web service

            df.to_sql("table_temp", engine)
            try:
                conn = psycopg2.connect(database='icfes-1', user='postgres', password='1234', host='localhost', port=5432)
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                # LIMPIEZA DE BD
                sql = """UPDATE table_temp SET "ESTU_ESTUDIANTE"='ESTUDIANTE' WHERE "ESTU_ESTUDIANTE" IS NULL;
                UPDATE table_temp SET "FAMI_TIENEAUTOMOVIL"='0' WHERE "FAMI_TIENEAUTOMOVIL"='No' OR "FAMI_TIENEAUTOMOVIL" IS NULL ;
                UPDATE table_temp SET "FAMI_TIENEAUTOMOVIL"='1' WHERE "FAMI_TIENEAUTOMOVIL"='Si';
                UPDATE table_temp SET "FAMI_TIENECOMPUTADOR"='0' WHERE "FAMI_TIENECOMPUTADOR"='No' OR "FAMI_TIENECOMPUTADOR" IS NULL;
                UPDATE table_temp SET "FAMI_TIENECOMPUTADOR"='1' WHERE "FAMI_TIENECOMPUTADOR"='Si' or "FAMI_TIENECOMPUTADOR"='3';
                UPDATE table_temp SET "FAMI_TIENEHORNOMICROOGAS"='0' WHERE "FAMI_TIENEHORNOMICROOGAS"='No' OR "FAMI_TIENEHORNOMICROOGAS" IS NULL;
                UPDATE table_temp SET "FAMI_TIENEHORNOMICROOGAS"='1' WHERE "FAMI_TIENEHORNOMICROOGAS"='Si';
                UPDATE table_temp SET "FAMI_TIENEINTERNET"='0' WHERE "FAMI_TIENEINTERNET"='No' OR "FAMI_TIENEINTERNET" IS NULL;
                UPDATE table_temp SET "FAMI_TIENEINTERNET"='1' WHERE "FAMI_TIENEINTERNET"='Si';
                UPDATE table_temp SET "FAMI_TIENELAVADORA"='0' WHERE "FAMI_TIENELAVADORA"='No' OR "FAMI_TIENELAVADORA" IS NULL;
                UPDATE table_temp SET "FAMI_TIENELAVADORA"='1' WHERE "FAMI_TIENELAVADORA"='Si';
                UPDATE table_temp SET "FAMI_TIENESERVICIOTV"='0' WHERE "FAMI_TIENESERVICIOTV"='No' OR "FAMI_TIENESERVICIOTV" IS NULL;
                UPDATE table_temp SET "FAMI_TIENESERVICIOTV"='1' WHERE "FAMI_TIENESERVICIOTV"='Si';
                UPDATE table_temp SET "FAMI_TIENECONSOLAVIDEOJUEGOS"='0' WHERE "FAMI_TIENECONSOLAVIDEOJUEGOS"='No' OR "FAMI_TIENECONSOLAVIDEOJUEGOS" IS NULL;
                UPDATE table_temp SET "FAMI_TIENECONSOLAVIDEOJUEGOS"='1' WHERE "FAMI_TIENECONSOLAVIDEOJUEGOS"='Si';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '1' Where "FAMI_EDUCACIONMADRE" = 'Ninguno' OR "FAMI_EDUCACIONMADRE"='No Aplica' OR "FAMI_EDUCACIONMADRE" IS NULL ;
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '2' Where "FAMI_EDUCACIONMADRE" = 'Primaria incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '3' Where "FAMI_EDUCACIONMADRE" = 'Primaria completa';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '4' Where "FAMI_EDUCACIONMADRE" = 'Secundaria (Bachillerato) incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '5' Where "FAMI_EDUCACIONMADRE" = 'Secundaria (Bachillerato) completa';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '6' Where "FAMI_EDUCACIONMADRE" = 'Técnica o tecnológica incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '7' Where "FAMI_EDUCACIONMADRE" = 'Técnica o tecnológica completa';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '8' Where "FAMI_EDUCACIONMADRE" = 'Educación profesional incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '9' Where "FAMI_EDUCACIONMADRE" = 'Educación profesional completa';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '10' Where "FAMI_EDUCACIONMADRE" = 'Postgrado';
                UPDATE table_temp SET "FAMI_EDUCACIONMADRE" = '11' Where "FAMI_EDUCACIONMADRE" = 'No sabe';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '1' Where "FAMI_EDUCACIONPADRE" = 'Ninguno' OR "FAMI_EDUCACIONPADRE"='No Aplica' OR "FAMI_EDUCACIONPADRE" IS NULL ;
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '2' Where "FAMI_EDUCACIONPADRE" = 'Primaria incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '3' Where "FAMI_EDUCACIONPADRE" = 'Primaria completa';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '4' Where "FAMI_EDUCACIONPADRE" = 'Secundaria (Bachillerato) incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '5' Where "FAMI_EDUCACIONPADRE" = 'Secundaria (Bachillerato) completa';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '6' Where "FAMI_EDUCACIONPADRE" = 'Técnica o tecnológica incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '7' Where "FAMI_EDUCACIONPADRE" = 'Técnica o tecnológica completa';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '8' Where "FAMI_EDUCACIONPADRE" = 'Educación profesional incompleta';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '9' Where "FAMI_EDUCACIONPADRE" = 'Educación profesional completa';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '10' Where "FAMI_EDUCACIONPADRE" = 'Postgrado';
                UPDATE table_temp SET "FAMI_EDUCACIONPADRE" = '11' Where "FAMI_EDUCACIONPADRE" = 'No sabe';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='1' where "FAMI_ESTRATOVIVIENDA"='Estrato 1' OR "FAMI_ESTRATOVIVIENDA"='Sin Estrato' OR "FAMI_ESTRATOVIVIENDA" IS NULL;
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='2' where "FAMI_ESTRATOVIVIENDA"='Estrato 2';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='3' where "FAMI_ESTRATOVIVIENDA"='Estrato 3';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='4' where "FAMI_ESTRATOVIVIENDA"='Estrato 4';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='5' where "FAMI_ESTRATOVIVIENDA"='Estrato 5';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='6' where "FAMI_ESTRATOVIVIENDA"='Estrato 6';
                UPDATE table_temp SET "FAMI_ESTRATOVIVIENDA"='7' where "FAMI_ESTRATOVIVIENDA"='Estrato 7';
                UPDATE table_temp SET "FAMI_PERSONASHOGAR"='2' where "FAMI_PERSONASHOGAR"='1 a 2' OR "FAMI_PERSONASHOGAR" IS NULL;
                UPDATE table_temp SET "FAMI_PERSONASHOGAR"='4' where "FAMI_PERSONASHOGAR"='3 a 4';
                UPDATE table_temp SET "FAMI_PERSONASHOGAR"='6' where "FAMI_PERSONASHOGAR"='5 a 6';
                UPDATE table_temp SET "FAMI_PERSONASHOGAR"='8' where "FAMI_PERSONASHOGAR"='7 a 8';
                UPDATE table_temp SET "FAMI_PERSONASHOGAR"='10' where "FAMI_PERSONASHOGAR"='9 o más';
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='1' where "FAMI_CUARTOSHOGAR"='Uno' OR "FAMI_CUARTOSHOGAR" IS NULL;
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='2' where "FAMI_CUARTOSHOGAR"='Dos';
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='3' where "FAMI_CUARTOSHOGAR"='Tres';
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='4' where "FAMI_CUARTOSHOGAR"='Cuatro';
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='5' where "FAMI_CUARTOSHOGAR"='Cinco';
                UPDATE table_temp SET "FAMI_CUARTOSHOGAR"='6' where "FAMI_CUARTOSHOGAR"='Seis o mas';
                UPDATE table_temp SET "COLE_JORNADA"='MANANA' WHERE "COLE_JORNADA"='MAÑANA';
                UPDATE table_temp SET "COLE_AREA_UBICACION"='R' WHERE "COLE_AREA_UBICACION"='RURAL';
                UPDATE table_temp SET "COLE_AREA_UBICACION"='U' WHERE "COLE_AREA_UBICACION"='URBANO';
                UPDATE table_temp SET "COLE_CARACTER"='ACADEMICO' WHERE "COLE_CARACTER"='ACADÉMICO';
                UPDATE table_temp SET "COLE_CARACTER"='TECNICO' WHERE "COLE_CARACTER"='TÉCNICO';
                UPDATE table_temp SET "COLE_CARACTER"='ACADEMICO Y TECNICO' WHERE "COLE_CARACTER"='TÉCNICO/ACADÉMICO';
                UPDATE table_temp SET "DESEMP_C_NATURALES"='00' WHERE "DESEMP_C_NATURALES" IS NULL;
                UPDATE table_temp SET "DESEMP_C_NATURALES"='INSUFICIENTE' WHERE "DESEMP_C_NATURALES"='1';
                UPDATE table_temp SET "DESEMP_C_NATURALES"='MINIMO' WHERE "DESEMP_C_NATURALES"='2';
                UPDATE table_temp SET "DESEMP_C_NATURALES"='SATISFACTORIO' WHERE "DESEMP_C_NATURALES"='3';
                UPDATE table_temp SET "DESEMP_C_NATURALES"='AVANZADO' WHERE "DESEMP_C_NATURALES"='4';
                UPDATE table_temp SET "DESEMP_LECTURA_CRITICA"='00' WHERE "DESEMP_LECTURA_CRITICA" IS NULL;
                UPDATE table_temp SET "DESEMP_LECTURA_CRITICA"='INSUFICIENTE' WHERE "DESEMP_LECTURA_CRITICA"='1';
                UPDATE table_temp SET "DESEMP_LECTURA_CRITICA"='MINIMO' WHERE "DESEMP_LECTURA_CRITICA"='2';
                UPDATE table_temp SET "DESEMP_LECTURA_CRITICA"='SATISFACTORIO' WHERE "DESEMP_LECTURA_CRITICA"='3';
                UPDATE table_temp SET "DESEMP_LECTURA_CRITICA"='AVANZADO' WHERE "DESEMP_LECTURA_CRITICA"='4';
                UPDATE table_temp SET "DESEMP_MATEMATICAS"='00' WHERE "DESEMP_MATEMATICAS" IS NULL;
                UPDATE table_temp SET "DESEMP_MATEMATICAS"='INSUFICIENTE' WHERE "DESEMP_MATEMATICAS"='1';
                UPDATE table_temp SET "DESEMP_MATEMATICAS"='MINIMO' WHERE "DESEMP_MATEMATICAS"='2';
                UPDATE table_temp SET "DESEMP_MATEMATICAS"='SATISFACTORIO' WHERE "DESEMP_MATEMATICAS"='3';
                UPDATE table_temp SET "DESEMP_MATEMATICAS"='AVANZADO' WHERE "DESEMP_MATEMATICAS"='4';
                UPDATE table_temp SET "DESEMP_SOCIALES_CIUDADANAS"='00' WHERE "DESEMP_SOCIALES_CIUDADANAS" IS NULL;
                UPDATE table_temp SET "DESEMP_SOCIALES_CIUDADANAS"='INSUFICIENTE' WHERE "DESEMP_SOCIALES_CIUDADANAS"='1';
                UPDATE table_temp SET "DESEMP_SOCIALES_CIUDADANAS"='MINIMO' WHERE "DESEMP_SOCIALES_CIUDADANAS"='2';
                UPDATE table_temp SET "DESEMP_SOCIALES_CIUDADANAS"='SATISFACTORIO' WHERE "DESEMP_SOCIALES_CIUDADANAS"='3';
                UPDATE table_temp SET "DESEMP_SOCIALES_CIUDADANAS"='AVANZADO' WHERE "DESEMP_SOCIALES_CIUDADANAS"='4';
                UPDATE table_temp SET "PERCENTIL_C_NATURALES"='00' WHERE "PERCENTIL_C_NATURALES" IS NULL;
                UPDATE table_temp SET "PERCENTIL_GLOBAL"='00' WHERE "PERCENTIL_GLOBAL" IS NULL;
                UPDATE table_temp SET "PERCENTIL_INGLES"='00' WHERE "PERCENTIL_INGLES" IS NULL;
                UPDATE table_temp SET "PERCENTIL_LECTURA_CRITICA"='00' WHERE "PERCENTIL_LECTURA_CRITICA" IS NULL;
                UPDATE table_temp SET "PERCENTIL_MATEMATICAS"='00' WHERE "PERCENTIL_MATEMATICAS" IS NULL;
                UPDATE table_temp SET "PERCENTIL_SOCIALES_CIUDADANAS"='00' WHERE "PERCENTIL_SOCIALES_CIUDADANAS" IS NULL;
                UPDATE table_temp SET "PUNT_C_NATURALES"='00' WHERE "PUNT_C_NATURALES" IS NULL;
                UPDATE table_temp SET "PUNT_SOCIALES_CIUDADANAS"='00' WHERE "PUNT_SOCIALES_CIUDADANAS" IS NULL;
                UPDATE table_temp SET "PUNT_GLOBAL"='00' WHERE "PUNT_GLOBAL" IS NULL;
                UPDATE table_temp SET "PUNT_LECTURA_CRITICA"='00' WHERE "PUNT_LECTURA_CRITICA" IS NULL;
                update table_temp set "COLE_MCPIO_UBICACION"='GUAlMATAN', "COLE_DEPTO_UBICACION"='NARIÑO', "COLE_JORNADA"='M', "COLE_CALENDARIO"='A', "COLE_NATURALEZA"='OFICIAL', "COLE_CARACTER"='ACADEMICO' where "COLE_CODIGO_ICFES"='011619' OR "COLE_CODIGO_ICFES"='031385' OR "COLE_CODIGO_ICFES"='111070';
                UPDATE table_temp SET "COLE_MCPIO_UBICACION"='CUASPUD CARLOSAMA' WHERE "COLE_MCPIO_UBICACION"='CUASPUD (CARLOSAMA)' OR "COLE_MCPIO_UBICACION"='CUASPÚD';
                UPDATE table_temp SET "COLE_MCPIO_UBICACION"='POTOSI' WHERE "COLE_MCPIO_UBICACION"='POTOSÍ';
                UPDATE table_temp SET "COLE_MCPIO_UBICACION"='CORDOBA' WHERE "COLE_MCPIO_UBICACION"='CÓRDOBA';
                UPDATE table_temp SET "ESTU_GENERO"='FEMENINO' WHERE "ESTU_GENERO"='F';
                UPDATE table_temp SET "ESTU_GENERO"='MASCULINO' WHERE "ESTU_GENERO"='M';
                UPDATE table_temp SET "FAMI_NUMLIBROS"='MAS DE 100 LIBROS' WHERE "FAMI_NUMLIBROS"='MÁS DE 100 LIBROS';
                
                ---Transformacion
                ALTER TABLE table_temp ALTER COLUMN "ESTU_FECHANACIMIENTO" TYPE date USING (trim("ESTU_FECHANACIMIENTO")::date);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_GLOBAL" TYPE int USING (trim("PUNT_GLOBAL")::int);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_LECTURA_CRITICA" TYPE int USING (trim("PUNT_LECTURA_CRITICA")::int);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_MATEMATICAS" TYPE int USING (trim("PUNT_MATEMATICAS")::int);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_C_NATURALES" TYPE int USING (trim("PUNT_C_NATURALES")::int);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_SOCIALES_CIUDADANAS" TYPE int USING (trim("PUNT_SOCIALES_CIUDADANAS")::int);
                ALTER TABLE table_temp ALTER COLUMN "PUNT_INGLES" TYPE int USING (trim("PUNT_INGLES")::int);
                ALTER TABLE table_temp ADD "ANO_NACIMIENTO" int;
                UPDATE table_temp SET "ANO_NACIMIENTO"=(SELECT EXTRACT(YEAR FROM "ESTU_FECHANACIMIENTO")) WHERE "ANO_NACIMIENTO" IS NULL;
                --ALTER TABLE table_temp ALTER COLUMN "ANO_NACIMIENTO" TYPE int USING (trim("ANO_NACIMIENTO")::int);
                ALTER TABLE table_temp ADD "ANO" int;
                UPDATE table_temp SET "ANO"='2017' WHERE "PERIODO"='20171' or "PERIODO"='20172';
                UPDATE table_temp SET "ANO"='2018' WHERE "PERIODO"='20181' or "PERIODO"='20182';
                UPDATE table_temp SET "ANO"='2019' WHERE "PERIODO"='20191' or "PERIODO"='20192' or "PERIODO" = '20193' or "PERIODO"='20194' or "PERIODO"='20195' or "PERIODO"='20196';
                UPDATE table_temp SET "ANO"='2020' WHERE "PERIODO"='20201' or "PERIODO"='20202' or "PERIODO" = '20203' or "PERIODO"='20204' or "PERIODO"='20205' or "PERIODO"='20206';
                UPDATE table_temp SET "ANO"='2021' WHERE "PERIODO"='20211' or "PERIODO"='20212' or "PERIODO" = '20213' or "PERIODO"='20214' or "PERIODO"='20215' or "PERIODO"='20216';
                UPDATE table_temp SET "ANO"='2022' WHERE "PERIODO"='20221' or "PERIODO"='20222' or "PERIODO" = '20223' or "PERIODO"='20224' or "PERIODO"='20225' or "PERIODO"='20226';
                UPDATE table_temp SET "ANO"='2023' WHERE "PERIODO"='20231' or "PERIODO"='20232' or "PERIODO" = '20233' or "PERIODO"='20234' or "PERIODO"='20235' or "PERIODO"='20236';
                UPDATE table_temp SET "ANO"='2024' WHERE "PERIODO"='20241' or "PERIODO"='20242' or "PERIODO" = '20243' or "PERIODO"='20244' or "PERIODO"='20245' or "PERIODO"='20246';
                UPDATE table_temp SET "ANO"='2025' WHERE "PERIODO"='20251' or "PERIODO"='20252' or "PERIODO" = '20253' or "PERIODO"='20254' or "PERIODO"='20255' or "PERIODO"='20256';
                UPDATE table_temp SET "ANO"='2026' WHERE "PERIODO"='20261' or "PERIODO"='20262' or "PERIODO" = '20263' or "PERIODO"='20264' or "PERIODO"='20265' or "PERIODO"='20266';
                UPDATE table_temp SET "ANO"='2027' WHERE "PERIODO"='20271' or "PERIODO"='20272' or "PERIODO" = '20273' or "PERIODO"='20274' or "PERIODO"='20275' or "PERIODO"='20276';
                UPDATE table_temp SET "ANO"='2028' WHERE "PERIODO"='20281' or "PERIODO"='20282' or "PERIODO" = '20283' or "PERIODO"='20284' or "PERIODO"='20285' or "PERIODO"='20286';
                UPDATE table_temp SET "ANO"='2029' WHERE "PERIODO"='20291' or "PERIODO"='20292' or "PERIODO" = '20293' or "PERIODO"='20294' or "PERIODO"='20295' or "PERIODO"='20296';
                UPDATE table_temp SET "ANO"='2030' WHERE "PERIODO"='20301' or "PERIODO"='20302' or "PERIODO" = '20303' or "PERIODO"='20304' or "PERIODO"='20305' or "PERIODO"='20306';
                --ALTER TABLE table_temp ALTER COLUMN "ANO" TYPE int USING (trim("ANO")::int);
                ALTER TABLE table_temp ADD "ESTU_EDAD" int;
                UPDATE table_temp SET "ESTU_EDAD"="ANO"-"ANO_NACIMIENTO";
                ALTER TABLE table_temp ADD "ESTU_RANGOEDAD" text;
                UPDATE table_temp SET "ESTU_RANGOEDAD"='MENORES DE 17' WHERE "ESTU_EDAD" < 17;
                UPDATE table_temp SET "ESTU_RANGOEDAD"='17' WHERE "ESTU_EDAD" = 17;
                UPDATE table_temp SET "ESTU_RANGOEDAD"='18 Y 19' WHERE "ESTU_EDAD" = 18 OR "ESTU_EDAD" = 19;
                UPDATE table_temp SET "ESTU_RANGOEDAD"='20 A 28' WHERE "ESTU_EDAD" >= 20 AND "ESTU_EDAD" <=28;
                UPDATE table_temp SET "ESTU_RANGOEDAD"='MAYORES DE 28' WHERE "ESTU_EDAD" > 28;
                ALTER TABLE table_temp ADD "FAMI_NIVEL_EDUCA_PADRES" int;
                ALTER TABLE table_temp ALTER COLUMN "FAMI_EDUCACIONMADRE" TYPE int USING (trim("FAMI_EDUCACIONMADRE")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_EDUCACIONPADRE" TYPE int USING (trim("FAMI_EDUCACIONPADRE")::int);
                UPDATE table_temp SET "FAMI_NIVEL_EDUCA_PADRES" = "FAMI_EDUCACIONPADRE";
                UPDATE table_temp SET "FAMI_NIVEL_EDUCA_PADRES" = "FAMI_EDUCACIONMADRE" WHERE "FAMI_EDUCACIONMADRE">"FAMI_EDUCACIONPADRE";
                ALTER TABLE table_temp ADD "FAMI_EDUCAPADRES" text;
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'NINGUNO' Where "FAMI_NIVEL_EDUCA_PADRES" = '1';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'PRIMARIA INCOMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '2';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'PRIMARIA COMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '3';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'SECUNDARIA BACHILLERATO IMCOMPLETO' Where "FAMI_NIVEL_EDUCA_PADRES" = '4';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'SECUNDARIA BACHILLERATO COMPLETO' Where "FAMI_NIVEL_EDUCA_PADRES" = '5';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'EDUCACION TECNICA O TECNOLOGICA INCOMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '6';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'EDUCACION TECNICA O TECNOLOGICA COMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '7';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'EDUCACION PROFECIONAL INCOMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '8';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'EDUCACION PROFECIONAL COMPLETA' Where "FAMI_NIVEL_EDUCA_PADRES" = '9';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'POSTGRADO' Where "FAMI_NIVEL_EDUCA_PADRES" = '10';
                UPDATE table_temp SET "FAMI_EDUCAPADRES" = 'NO SABE' Where "FAMI_NIVEL_EDUCA_PADRES" = '11';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'HOGAR' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja en el hogar, no trabaja o estudia';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPLEADO OBRERO U OPERARIO' WHERE "FAMI_TRABAJOLABORPADRE"='Es operario de máquinas o conduce vehículos (taxita, chofer)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPLEADO CON CARGO COMO DIRECTOR O GERENTE GENERAL' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPLEADO DE NIVEL AUXILIAR O ADMINISTRATIVO' WHERE "FAMI_TRABAJOLABORPADRE"='Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPLEADO DE NIVEL DIRECTIVO' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPLEADO DE NIVEL TECNICO O PROFESIONAL' WHERE "FAMI_TRABAJOLABORPADRE"='Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'PROFESIONAL INDEPENDIENTE' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'EMPRESARIO' WHERE "FAMI_TRABAJOLABORPADRE"='Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'OTRA ACTIVIDAD U OCUPACION' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja como personal de limpieza, mantenimiento, seguridad o construcción' OR "FAMI_TRABAJOLABORPADRE"='Es vendedor o trabaja en atención al público' OR "FAMI_TRABAJOLABORPADRE"='Es agricultor, pesquero o jornalero' OR "FAMI_TRABAJOLABORPADRE"='No aplica' OR "FAMI_TRABAJOLABORPADRE"='No sabe' OR "FAMI_TRABAJOLABORPADRE" IS NULL;
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'PENSIONADO' WHERE "FAMI_TRABAJOLABORPADRE"='Pensionado';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'PEQUENO EMPRESARIO' WHERE "FAMI_TRABAJOLABORPADRE"='Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc';
                UPDATE table_temp SET "FAMI_TRABAJOLABORPADRE" = 'TRABAJADOR POR CUENTA PROPIA' WHERE "FAMI_TRABAJOLABORPADRE"='Trabaja por cuenta propia (por ejemplo plomero, electricista)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'HOGAR' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja en el hogar, no trabaja o estudia';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPLEADO OBRERO U OPERARIO' WHERE "FAMI_TRABAJOLABORMADRE"='Es operario de máquinas o conduce vehículos (taxita, chofer)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPLEADO CON CARGO COMO DIRECTOR O GERENTE GENERAL' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPLEADO DE NIVEL AUXILIAR O ADMINISTRATIVO' WHERE "FAMI_TRABAJOLABORMADRE"='Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPLEADO DE NIVEL DIRECTIVO' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPLEADO DE NIVEL TECNICO O PROFESIONAL' WHERE "FAMI_TRABAJOLABORMADRE"='Tiene un trabajo de tipo auxiliar administrativo (por ejemplo, secretario o asistente)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'PROFESIONAL INDEPENDIENTE' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja como profesional (por ejemplo médico, abogado, ingeniero)';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'EMPRESARIO' WHERE "FAMI_TRABAJOLABORMADRE"='Es dueño de un negocio grande, tiene un cargo de nivel directivo o gerencial';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'OTRA ACTIVIDAD U OCUPACION' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja como personal de limpieza, mantenimiento, seguridad o construcción' OR "FAMI_TRABAJOLABORMADRE"='Es vendedor o trabaja en atención al público' OR "FAMI_TRABAJOLABORMADRE"='Es agricultor, pesquero o jornalero' OR "FAMI_TRABAJOLABORMADRE"='No aplica' OR "FAMI_TRABAJOLABORMADRE"='No sabe' OR "FAMI_TRABAJOLABORMADRE" IS NULL;
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'PENSIONADO' WHERE "FAMI_TRABAJOLABORMADRE"='Pensionado';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'PEQUENO EMPRESARIO' WHERE "FAMI_TRABAJOLABORMADRE"='Es dueño de un negocio pequeño (tiene pocos empleados o no tiene, por ejemplo tienda, papelería, etc';
                UPDATE table_temp SET "FAMI_TRABAJOLABORMADRE" = 'TRABAJADOR POR CUENTA PROPIA' WHERE "FAMI_TRABAJOLABORMADRE"='Trabaja por cuenta propia (por ejemplo plomero, electricista)';
                ALTER TABLE table_temp ADD "ECO_CONDICION_VIVE" text;
                ALTER TABLE table_temp ADD "IND_ECO_CONDICION_VIVE" decimal;
                ALTER TABLE table_temp ALTER COLUMN "FAMI_PERSONASHOGAR" TYPE int USING (trim("FAMI_PERSONASHOGAR")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_CUARTOSHOGAR" TYPE int USING (trim("FAMI_CUARTOSHOGAR")::int);
                UPDATE table_temp SET "IND_ECO_CONDICION_VIVE" = ("FAMI_PERSONASHOGAR")/("FAMI_CUARTOSHOGAR");
                UPDATE table_temp SET "ECO_CONDICION_VIVE" = 'SIN HACINAMIENTO' Where  "IND_ECO_CONDICION_VIVE" <= 2.4 ;
                UPDATE table_temp SET "ECO_CONDICION_VIVE" = 'HACINAMIENTO MEDIO' Where "IND_ECO_CONDICION_VIVE" >=  2.5  AND "IND_ECO_CONDICION_VIVE"<=4.9;
                UPDATE table_temp SET "ECO_CONDICION_VIVE" = 'HACINAMIENTO CRITICO' Where  "IND_ECO_CONDICION_VIVE" >  4.9 ;
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENECONSOLAVIDEOJUEGOS" TYPE int USING (trim("FAMI_TIENECONSOLAVIDEOJUEGOS")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENECOMPUTADOR" TYPE int USING (trim("FAMI_TIENECOMPUTADOR")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENEINTERNET" TYPE int USING (trim("FAMI_TIENEINTERNET")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENESERVICIOTV" TYPE int USING (trim("FAMI_TIENESERVICIOTV")::int);
                ALTER TABLE table_temp ADD "IND_ECO_CONDICION_TIC" int;
                ALTER TABLE table_temp ADD "ECO_CONDICION_TIC" text;
                UPDATE table_temp SET "IND_ECO_CONDICION_TIC" = ("FAMI_TIENECONSOLAVIDEOJUEGOS")+("FAMI_TIENECOMPUTADOR")+("FAMI_TIENEINTERNET")+("FAMI_TIENESERVICIOTV");
                UPDATE table_temp SET "ECO_CONDICION_TIC" = 'BUENA' WHERE "IND_ECO_CONDICION_TIC"= '5' OR "IND_ECO_CONDICION_TIC"= '4';
                UPDATE table_temp SET "ECO_CONDICION_TIC" = 'REGULAR' WHERE "IND_ECO_CONDICION_TIC"= '2' OR "IND_ECO_CONDICION_TIC"= '3';
                UPDATE table_temp SET "ECO_CONDICION_TIC" = 'MALA' WHERE "IND_ECO_CONDICION_TIC"= '0' OR "IND_ECO_CONDICION_TIC"= '1';
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENELAVADORA" TYPE int USING (trim("FAMI_TIENELAVADORA")::int);
                ALTER TABLE table_temp ALTER COLUMN "FAMI_TIENEHORNOMICROOGAS" TYPE int USING (trim("FAMI_TIENEHORNOMICROOGAS")::int);
                ALTER TABLE table_temp ADD "IND_ECO_CONDICION_ELECTRODOMESTICOS" int;
                ALTER TABLE table_temp ADD "ECO_CONDICION_ELECTRODOMESTICOS" text;
                UPDATE table_temp SET "IND_ECO_CONDICION_ELECTRODOMESTICOS" = ("FAMI_TIENELAVADORA")+("FAMI_TIENEHORNOMICROOGAS")+("FAMI_TIENESERVICIOTV");
                UPDATE table_temp SET "ECO_CONDICION_ELECTRODOMESTICOS" = 'BUENA' WHERE "IND_ECO_CONDICION_ELECTRODOMESTICOS"= '3';
                UPDATE table_temp SET "ECO_CONDICION_ELECTRODOMESTICOS" = 'REGULAR' WHERE "IND_ECO_CONDICION_ELECTRODOMESTICOS"= '2';
                UPDATE table_temp SET "ECO_CONDICION_ELECTRODOMESTICOS" = 'MALA' WHERE "IND_ECO_CONDICION_ELECTRODOMESTICOS"= '0' OR "IND_ECO_CONDICION_ELECTRODOMESTICOS"= '1';
                ALTER TABLE table_temp ADD "PROM_REND" int;
                UPDATE table_temp SET "PROM_REND" = ("PUNT_GLOBAL")/5;
                ALTER TABLE table_temp ALTER COLUMN "ANO" SET DATA TYPE text;
                do $$
                declare
                conta1 integer;
                uno integer;
                conta integer;
                orden_sql text;
                orden_sql1 text;
                orden_sql2 text;
                orden_sql3 text;
                orden_sql4 text;
                orden_sql5 text;
                orden_sql6 text;
                orden_sql7 text;
                orden_sql8 text;
                begin
                conta1 := count(*) from fact_saber11;
                uno := 1;
                conta := conta1+uno;
                orden_sql := 'create sequence sequen start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql;
                orden_sql1 := 'create sequence sequen1 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql1;
                orden_sql2 := 'create sequence sequen2 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql2;
                orden_sql3 := 'create sequence sequen3 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql3;
                orden_sql4 := 'create sequence sequen4 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql4;
                orden_sql5 := 'create sequence sequen5 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql5;
                orden_sql6 := 'create sequence sequen6 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql6;
                orden_sql7 := 'create sequence sequen7 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql7;
                orden_sql8 := 'create sequence sequen8 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
                execute orden_sql8;
                end $$;
                alter table fact_saber11 alter column id_estudiante set default nextval('sequen');
                alter table fact_saber11 alter column id_institucion set default nextval('sequen1');
                alter table fact_saber11 alter column id_lugar set default nextval('sequen2');
                alter table fact_saber11 alter column id_pru_c_nat set default nextval('sequen3');
                alter table fact_saber11 alter column id_pru_ingles set default nextval('sequen4');
                alter table fact_saber11 alter column id_pru_lec_crit set default nextval('sequen5');
                alter table fact_saber11 alter column id_pru_mat set default nextval('sequen6');
                alter table fact_saber11 alter column id_pru_soc_ciu set default nextval('sequen7');
                alter table fact_saber11 alter column id_tiempo set default nextval('sequen8');
                ---incersion de datos
                insert into dim_estudiantes(
                eco_condicion_electrodomesticos,
                eco_condicion_tic,
                eco_condicion_vive,
                estu_consecutivo,
                estu_genero,
                estu_rango_edad,
                fami_estrato_vivienda,
                fami_max_nivel_educa_padres,
                fami_ocup_madre,
                fami_ocup_padre)
                select
                "ECO_CONDICION_ELECTRODOMESTICOS",
                "ECO_CONDICION_TIC",
                "ECO_CONDICION_VIVE",
                "ESTU_CONSECUTIVO",
                "ESTU_GENERO",
                "ESTU_RANGOEDAD",
                "FAMI_ESTRATOVIVIENDA",
                "FAMI_EDUCAPADRES",
                "FAMI_TRABAJOLABORMADRE",
                "FAMI_TRABAJOLABORPADRE"
                from table_temp;
                insert into dim_instituciones (
                cole_bilingue,
                cole_caracter,
                cole_genero,
                cole_jornada,
                cole_naturaleza,
                cole_nombre_sede,
                cole_calendario)
                select
                "COLE_BILINGUE",
                "COLE_CARACTER",
                "COLE_GENERO",
                "COLE_JORNADA",
                "COLE_NATURALEZA",
                "COLE_NOMBRE_SEDE",
                "COLE_CALENDARIO"
                from table_temp;
                insert into dim_lugares (
                cole_area_ubicacion,
                cole_mcpio_ubicacion,
                estu_mcpio_presentacion,
                estu_reside_mcpio)
                select
                "COLE_AREA_UBICACION",
                "COLE_MCPIO_UBICACION",
                "ESTU_MCPIO_PRESENTACION",
                "ESTU_MCPIO_RESIDE"
                from table_temp;
                insert into dim_pru_c_nat (
                desemp_c_naturales)
                select
                "DESEMP_C_NATURALES"
                from table_temp;
                insert into dim_pru_ingles (
                desemp_ingles)
                select
                "DESEMP_INGLES"
                from table_temp;
                insert into dim_pru_lec_crit (
                desemp_lec_crit)
                select
                "DESEMP_LECTURA_CRITICA"
                from table_temp;
                insert into dim_pru_mat (
                desemp_mat)
                select
                "DESEMP_MATEMATICAS"
                from table_temp;
                insert into dim_pru_soc_ciu (
                desemp_soc_ciu)
                select
                "DESEMP_SOCIALES_CIUDADANAS"
                from table_temp;
                insert into dim_tiempo (
                ano)
                select
                "ANO"
                from table_temp;
                insert into fact_saber11 (
                punt_global,
                prom_rend,
                punt_c_nat,
                punt_ingles,
                punt_lec_crit,
                punt_mat, 
                punt_soc_ciu) 
                select 
                "PUNT_GLOBAL", 
                "PROM_REND",
                "PUNT_C_NATURALES",
                "PUNT_INGLES",
                "PUNT_LECTURA_CRITICA",
                "PUNT_MATEMATICAS",
                "PUNT_SOCIALES_CIUDADANAS"
                from table_temp;
                drop sequence sequen cascade;
                drop sequence sequen1 cascade;
                drop sequence sequen2 cascade;
                drop sequence sequen3 cascade;
                drop sequence sequen4 cascade;
                drop sequence sequen5 cascade;
                drop sequence sequen6 cascade;
                drop sequence sequen7 cascade;
                drop sequence sequen8 cascade;
                DROP TABLE table_temp;
                DELETE FROM "Dashboard_entrada";"""

                cur.execute(sql)
            except (Exception, psycopg2.OperationalError) as error:
                print(error)
            # row = cur.fetchall()
            # print(row)
            cur.close()
            conn.commit()
            conn.close()
            from shutil import rmtree
            rmtree(BASE_DIR+'/media/icfes')
            # print(df)
            messages.success(request, 'Carga de Archivo Exitoso!')
            return render(request, "Dashboard/subir.html")
         else:
             messages.error(request, "Error al procesar el formulario")
             return render(request, "Dashboard/subir.html")
    else:
        messages.error(request, " ")
        return render(request, "Dashboard/subir.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
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
    sql = "select distinct(ano) from dim_tiempo order by ano;"
    cur.execute(sql)
    row = cur.fetchall()
    cur.close()
    conn.close()
    ano = row

    context = {
        'object': inst,
        'muni': muni,
        'ano': ano,

    }
    return render(request, "Dashboard/gestion.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def Gestion(request):
    label = []
    dato = []
    contador = []
    # se obtiene todas las variables desde el html desde un form con el metodo get
    message = request.GET['municipio']
    puntaje = request.GET['puntaje']
    inst = request.GET['inst']
    ano = request.GET['ano']
    if (ano == "TODOS"):
        if (message == "TODOS"):
            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(prom=Round(Avg(puntaje)),
                                                                                           conta=Count(
                                                                                               puntaje)).order_by(
                'id_lugar__cole_mcpio_ubicacion')
            for entry in result:
                label.append(entry['id_lugar__cole_mcpio_ubicacion']+ " : " + entry['id_tiempo__ano'])  # guarda nombre del departamento ya agrupado
                dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                contador.append(entry['conta'])
        else:
            if (inst == "General"):
                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede', 'id_tiempo__ano').annotate(prom=Round(Avg(puntaje)),
                                                                                                 conta=Count(
                                                                                                     puntaje)).filter(
                    id_lugar__cole_mcpio_ubicacion=message).order_by('id_lugar__cole_mcpio_ubicacion')
            else:
                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Round(Avg(puntaje)),
                                                                                                 conta=Count(
                                                                                                     puntaje)).filter(
                    id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by('id_lugar__cole_mcpio_ubicacion')
            for entry in result:
                label.append(entry['id_institucion__cole_nombre_sede']+ " : " + entry['id_tiempo__ano'])  # guarda nombre del departamento ya agrupado
                dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por inst)
                contador.append(entry['conta'])
    else:
            if (message == "TODOS"):
                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion').annotate(prom=Round(Avg(puntaje)),
                                                                                               conta=Count(
                                                                                                   puntaje)).filter(
                    id_tiempo__ano=ano).order_by('id_lugar__cole_mcpio_ubicacion')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'])  # guarda nombre del departamento ya agrupado
                    dato.append(entry['prom'])  # guarda promedio de cada grupo creado(por municipio)
                    contador.append(entry['conta'])
            else:
                if (inst == "General"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Round(Avg(puntaje)),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by('id_lugar__cole_mcpio_ubicacion')
                else:
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede').annotate(prom=Round(Avg(puntaje)),
                                                                                                     conta=Count(
                                                                                                         puntaje)).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano,
                        id_institucion__cole_nombre_sede=inst).order_by('id_lugar__cole_mcpio_ubicacion')
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
@allowed_users(allowed_roles=['admin','usuario'])
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
    return render(request, "Dashboard/gestionC.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def GestionC(request):
    label = []
    Cmasculino = []
    Cfemenino = []
    Cticbuena = []
    Cticregular = []
    Cticmala = []
    CHmedio = []
    CHcritico = []
    CHsin = []
    Ce17 = []
    Ce18y19 = []
    Ce20a28 = []
    Cemayoresde28 = []
    Cemenoresde17 = []
    Ces1 = []
    Ces2 = []
    Ces3 = []
    Ces4 = []
    Ces5 = []
    Ces6 = []
    CEPC = []
    CEPI = []
    CETC = []
    CETI = []
    Cn = []
    Cnosabe = []
    Cpostgrado = []
    CPC = []
    CPI = []
    CBC = []
    CBI = []
    # se obtiene todas las variables desde el html desde un form con el metodo get
    message = request.GET['municipio']
    inst = request.GET['inst']
    ano = request.GET['ano']
    categoria = request.GET['categoria']

    if (ano == "TODOS"):
        if (message == "TODOS"):
            if (categoria == "Genero"):

                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).order_by(
                    'id_lugar__cole_mcpio_ubicacion')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                    Cfemenino.append(entry['conta1'])
                    Cmasculino.append(entry['conta2'])
            else:
                if (categoria == "Condicion de las TIC"):

                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                        conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).order_by(
                        'id_lugar__cole_mcpio_ubicacion')
                    for entry in result:
                        label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                        Cticbuena.append(entry['conta1'])
                        Cticregular.append(entry['conta2'])
                        Cticmala.append(entry['conta3'])

                else:
                    if (categoria == "Condicion en la que vive"):

                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                            'id_tiempo__ano').annotate(
                            conta1=Count('id_estudiante',
                                         filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                            conta2=Count('id_estudiante',
                                         filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                            conta3=Count('id_estudiante',
                                         filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).order_by(
                            'id_lugar__cole_mcpio_ubicacion')
                        for entry in result:
                            label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                            CHmedio.append(entry['conta1'])
                            CHcritico.append(entry['conta2'])
                            CHsin.append(entry['conta3'])

                    else:
                        if (categoria == "Rango de Edad"):

                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                'id_tiempo__ano').annotate(
                                conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                conta4=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                conta5=Count('id_estudiante',
                                             filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).order_by(
                                'id_tiempo__ano', 'id_lugar__cole_mcpio_ubicacion')
                            for entry in result:
                                label.append(entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                Ce17.append(entry['conta1'])
                                Ce18y19.append(entry['conta2'])
                                Ce20a28.append(entry['conta3'])
                                Cemayoresde28.append(entry['conta4'])
                                Cemenoresde17.append(entry['conta5'])

                        else:
                            if (categoria == "Estrato"):

                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                    'id_tiempo__ano').annotate(
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="1")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="2")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="3")),
                                    conta4=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="4")),
                                    conta5=Count('id_estudiante', filter=Q(id_estudiante__fami_estrato_vivienda="5")),
                                    conta6=Count('id_estudiante',
                                                 filter=Q(id_estudiante__fami_estrato_vivienda="6"))).order_by(
                                    'id_lugar__cole_mcpio_ubicacion')
                                for entry in result:
                                    label.append(
                                        entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                    Ces1.append(entry['conta1'])
                                    Ces2.append(entry['conta2'])
                                    Ces3.append(entry['conta3'])
                                    Ces4.append(entry['conta4'])
                                    Ces5.append(entry['conta5'])
                                    Ces6.append(entry['conta6'])
                            else:
                                if (categoria == "Nivel Educativo Padres"):

                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                        'id_tiempo__ano').annotate(
                                        conta1=Count('id_estudiante',
                                                     filter=Q(id_estudiante__fami_max_nivel_educa_padres="NINGUNO")),
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
                                                      filter=Q(id_estudiante__fami_max_nivel_educa_padres="POSTGRADO")),
                                        conta11=Count('id_estudiante',
                                                      filter=Q(id_estudiante__fami_max_nivel_educa_padres="NO SABE"))
                                    ).order_by(
                                        'id_lugar__cole_mcpio_ubicacion')
                                    for entry in result:
                                        label.append(
                                            entry['id_lugar__cole_mcpio_ubicacion'] + " : " + entry['id_tiempo__ano'])
                                        Cn.append(entry['conta1'])
                                        CPI.append(entry['conta2'])
                                        CPC.append(entry['conta3'])
                                        CBI.append(entry['conta4'])
                                        CBC.append(entry['conta5'])
                                        CETI.append(entry['conta6'])
                                        CETC.append(entry['conta7'])
                                        CEPI.append(entry['conta8'])
                                        CEPC.append(entry['conta9'])
                                        Cpostgrado.append(entry['conta10'])
                                        Cnosabe.append(entry['conta11'])

        else:
            if (inst == "General"):
                if (categoria == "Genero"):
                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede', 'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message).order_by('id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])

                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                            Cticbuena.append(entry['conta1'])
                            Cticregular.append(entry['conta2'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
                                conta1=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO MEDIO")),
                                conta2=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="HACINAMIENTO CRITICO")),
                                conta3=Count('id_estudiante',
                                             filter=Q(id_estudiante__eco_condicion_vive="SIN HACINAMIENTO"))).filter(
                                id_lugar__cole_mcpio_ubicacion=message).order_by(
                                'id_institucion__cole_nombre_sede')
                            for entry in result:
                                label.append(
                                    entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                CHmedio.append(entry['conta1'])
                                CHcritico.append(entry['conta2'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
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
                                    Ce17.append(entry['conta1'])
                                    Ce18y19.append(entry['conta2'])
                                    Ce20a28.append(entry['conta3'])
                                    Cemayoresde28.append(entry['conta4'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
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
                                        Ces1.append(entry['conta1'])
                                        Ces2.append(entry['conta2'])
                                        Ces3.append(entry['conta3'])
                                        Ces4.append(entry['conta4'])
                                        Ces5.append(entry['conta5'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
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
                                            Cn.append(entry['conta1'])
                                            CPI.append(entry['conta2'])
                                            CPC.append(entry['conta3'])
                                            CBI.append(entry['conta4'])
                                            CBC.append(entry['conta5'])
                                            CETI.append(entry['conta6'])
                                            CETC.append(entry['conta7'])
                                            CEPI.append(entry['conta8'])
                                            CEPC.append(entry['conta9'])
                                            Cpostgrado.append(entry['conta10'])
                                            Cnosabe.append(entry['conta11'])
            else:
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede', 'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                        'id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                            Cticbuena.append(entry['conta1'])
                            Cticregular.append(entry['conta2'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
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
                                CHmedio.append(entry['conta1'])
                                CHcritico.append(entry['conta2'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
                                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="17")),
                                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="18 Y 19")),
                                    conta3=Count('id_estudiante', filter=Q(id_estudiante__estu_rango_edad="20 A 28")),
                                    conta4=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MAYORES DE 28")),
                                    conta5=Count('id_estudiante',
                                                 filter=Q(id_estudiante__estu_rango_edad="MENORES DE 17"))).filter(
                                    id_lugar__cole_mcpio_ubicacion=message,
                                    id_institucion__cole_nombre_sede=inst).order_by(
                                    'id_tiempo__ano', 'id_institucion__cole_nombre_sede')
                                for entry in result:
                                    label.append(
                                        entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                    Ce17.append(entry['conta1'])
                                    Ce18y19.append(entry['conta2'])
                                    Ce20a28.append(entry['conta3'])
                                    Cemayoresde28.append(entry['conta4'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
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
                                        id_institucion__cole_nombre_sede=inst).order_by(
                                        'id_institucion__cole_nombre_sede')
                                    for entry in result:
                                        label.append(
                                            entry['id_institucion__cole_nombre_sede'] + " : " + entry['id_tiempo__ano'])
                                        Ces1.append(entry['conta1'])
                                        Ces2.append(entry['conta2'])
                                        Ces3.append(entry['conta3'])
                                        Ces4.append(entry['conta4'])
                                        Ces5.append(entry['conta5'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
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
                                            id_institucion__cole_nombre_sede=inst).order_by(
                                            'id_institucion__cole_nombre_sede')
                                        for entry in result:
                                            label.append(
                                                entry['id_institucion__cole_nombre_sede'] + " : " + entry[
                                                    'id_tiempo__ano'])
                                            Cn.append(entry['conta1'])
                                            CPI.append(entry['conta2'])
                                            CPC.append(entry['conta3'])
                                            CBI.append(entry['conta4'])
                                            CBC.append(entry['conta5'])
                                            CETI.append(entry['conta6'])
                                            CETC.append(entry['conta7'])
                                            CEPI.append(entry['conta8'])
                                            CEPC.append(entry['conta9'])
                                            Cpostgrado.append(entry['conta10'])
                                            Cnosabe.append(entry['conta11'])


    else:
        if (message == "TODOS"):
            if (categoria == "Genero"):

                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion', 'id_tiempo__ano').annotate(
                    conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                    conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                    id_tiempo__ano=ano).order_by(
                    'id_lugar__cole_mcpio_ubicacion')
                for entry in result:
                    label.append(entry['id_lugar__cole_mcpio_ubicacion'])
                    Cfemenino.append(entry['conta1'])
                    Cmasculino.append(entry['conta2'])
            else:
                if (categoria == "Condicion de las TIC"):
                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                        'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                        conta3=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                        id_tiempo__ano=ano).order_by(
                        'id_lugar__cole_mcpio_ubicacion')
                    for entry in result:
                        label.append(entry['id_lugar__cole_mcpio_ubicacion'])
                        Cticbuena.append(entry['conta1'])
                        Cticregular.append(entry['conta2'])
                        Cticmala.append(entry['conta3'])

                else:
                    if (categoria == "Condicion en la que vive"):
                        result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                            'id_tiempo__ano').annotate(
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
                            CHmedio.append(entry['conta1'])
                            CHcritico.append(entry['conta2'])
                            CHsin.append(entry['conta3'])

                    else:
                        if (categoria == "Rango de Edad"):
                            result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                'id_tiempo__ano').annotate(
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
                                Ce17.append(entry['conta1'])
                                Ce18y19.append(entry['conta2'])
                                Ce20a28.append(entry['conta3'])
                                Cemayoresde28.append(entry['conta4'])
                                Cemenoresde17.append(entry['conta5'])

                        else:
                            if (categoria == "Estrato"):
                                result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                    'id_tiempo__ano').annotate(
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
                                    Ces1.append(entry['conta1'])
                                    Ces2.append(entry['conta2'])
                                    Ces3.append(entry['conta3'])
                                    Ces4.append(entry['conta4'])
                                    Ces5.append(entry['conta5'])
                                    Ces6.append(entry['conta6'])
                            else:
                                if (categoria == "Nivel Educativo Padres"):
                                    result = FactSaber11.objects.values('id_lugar__cole_mcpio_ubicacion',
                                                                        'id_tiempo__ano').annotate(
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
                                        Cn.append(entry['conta1'])
                                        CPI.append(entry['conta2'])
                                        CPC.append(entry['conta3'])
                                        CBI.append(entry['conta4'])
                                        CBC.append(entry['conta5'])
                                        CETI.append(entry['conta6'])
                                        CETC.append(entry['conta7'])
                                        CEPI.append(entry['conta8'])
                                        CEPC.append(entry['conta9'])
                                        Cpostgrado.append(entry['conta10'])
                                        Cnosabe.append(entry['conta11'])


        else:
            if (inst == "General"):
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                        'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                        'id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante',
                                         filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_tiempo__ano=ano).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            Cticbuena.append(entry['conta1'])
                            Cticregular.append(entry['conta2'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion de la vivienda"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
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
                                CHmedio.append(entry['conta1'])
                                CHcritico.append(entry['conta2'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
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
                                    Ce17.append(entry['conta1'])
                                    Ce18y19.append(entry['conta2'])
                                    Ce20a28.append(entry['conta3'])
                                    Cemayoresde28.append(entry['conta4'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
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
                                        Ces1.append(entry['conta1'])
                                        Ces2.append(entry['conta2'])
                                        Ces3.append(entry['conta3'])
                                        Ces4.append(entry['conta4'])
                                        Ces5.append(entry['conta5'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
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
                                            Cn.append(entry['conta1'])
                                            CPI.append(entry['conta2'])
                                            CPC.append(entry['conta3'])
                                            CBI.append(entry['conta4'])
                                            CBC.append(entry['conta5'])
                                            CETI.append(entry['conta6'])
                                            CETC.append(entry['conta7'])
                                            CEPI.append(entry['conta8'])
                                            CEPC.append(entry['conta9'])
                                            Cpostgrado.append(entry['conta10'])
                                            Cnosabe.append(entry['conta11'])
            else:
                if (categoria == "Genero"):

                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                        'id_tiempo__ano').annotate(
                        conta1=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="FEMENINO")),
                        conta2=Count('id_estudiante', filter=Q(id_estudiante__estu_genero="MASCULINO"))).filter(
                        id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                        id_tiempo__ano=ano).order_by(
                        'id_institucion__cole_nombre_sede')
                    for entry in result:
                        label.append(entry['id_institucion__cole_nombre_sede'])
                        Cfemenino.append(entry['conta1'])
                        Cmasculino.append(entry['conta2'])
                else:
                    if (categoria == "Condicion de las TIC"):
                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                            'id_tiempo__ano').annotate(
                            conta1=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="BUENA")),
                            conta2=Count('id_estudiante', filter=Q(id_estudiante__eco_condicion_tic="REGULAR")),
                            conta3=Count('id_estudiante',
                                         filter=Q(id_estudiante__eco_condicion_tic="MALA"))).filter(
                            id_lugar__cole_mcpio_ubicacion=message, id_institucion__cole_nombre_sede=inst,
                            id_tiempo__ano=ano).order_by(
                            'id_institucion__cole_nombre_sede')
                        for entry in result:
                            label.append(
                                entry['id_institucion__cole_nombre_sede'])
                            Cticbuena.append(entry['conta1'])
                            Cticregular.append(entry['conta2'])
                            Cticmala.append(entry['conta3'])

                    else:
                        if (categoria == "Condicion en la que vive"):
                            result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                'id_tiempo__ano').annotate(
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
                                CHmedio.append(entry['conta1'])
                                CHcritico.append(entry['conta2'])
                                CHsin.append(entry['conta3'])

                        else:
                            if (categoria == "Rango de Edad"):
                                result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                    'id_tiempo__ano').annotate(
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
                                    Ce17.append(entry['conta1'])
                                    Ce18y19.append(entry['conta2'])
                                    Ce20a28.append(entry['conta3'])
                                    Cemayoresde28.append(entry['conta4'])
                                    Cemenoresde17.append(entry['conta5'])

                            else:
                                if (categoria == "Estrato"):
                                    result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                        'id_tiempo__ano').annotate(
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
                                        Ces1.append(entry['conta1'])
                                        Ces2.append(entry['conta2'])
                                        Ces3.append(entry['conta3'])
                                        Ces4.append(entry['conta4'])
                                        Ces5.append(entry['conta5'])
                                        Ces6.append(entry['conta6'])
                                else:
                                    if (categoria == "Nivel Educativo Padres"):
                                        result = FactSaber11.objects.values('id_institucion__cole_nombre_sede',
                                                                            'id_tiempo__ano').annotate(
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
                                            Cn.append(entry['conta1'])
                                            CPI.append(entry['conta2'])
                                            CPC.append(entry['conta3'])
                                            CBI.append(entry['conta4'])
                                            CBC.append(entry['conta5'])
                                            CETI.append(entry['conta6'])
                                            CETC.append(entry['conta7'])
                                            CEPI.append(entry['conta8'])
                                            CEPC.append(entry['conta9'])
                                            Cpostgrado.append(entry['conta10'])
                                            Cnosabe.append(entry['conta11'])

    return JsonResponse(data={

        'labels': label,
        'Cmasculino': Cmasculino,
        'Cfemenino': Cfemenino,
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
def crear(request):
    return render(request, "Dashboard/crear.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
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
@allowed_users(allowed_roles=['admin','usuario'])
def punt_anio(request):
    label = []
    puntaje = []

    result = FactSaber11.objects.values('id_tiempo__ano').annotate(Count('id_tiempo__ano'),
                                                                   prom=Avg('punt_global')).order_by('id_tiempo__ano')
    for entry in result:
        puntaje.append(entry['prom'])
        label.append(entry['id_tiempo__ano'])

    return JsonResponse(data={
        'labels': label,
        'puntajes': puntaje
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','usuario'])
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
@allowed_users(allowed_roles=['admin','usuario'])
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
@allowed_users(allowed_roles=['admin','usuario'])
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
@allowed_users(allowed_roles=['admin','usuario'])
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
@allowed_users(allowed_roles=['admin','usuario'])
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
