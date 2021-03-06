"""Proyecto1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Dashboard.GeneralDashboard import viewsGeneral
from Dashboard.cubos import viewsCubos
from Dashboard import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from Dashboard.views import Prueba

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.obando, name='obando'),
    path('inicio/', views.inicio),
    path('obando/', views.obando, name="obando"),
    path('gestion/', views.gestionHtml, name="gestion"),
    path('gestion-data/', views.Gestion, name='Gestion'),
    path('gestionC-data/', views.GestionC, name='GestionC'),
    path('gestionC/', views.gestionCHtml, name='gestionC'),
    # path('prueba/', Prueba.as_view()),
    path('punt-anio/', views.punt_anio, name='punt-anio'),
    path('tot-est/', views.tot_est, name='tot-est'),
    path('grafic-prin/', views.grafic_principal, name='grafic-prin'),
    path('lect-CriticC/', views.critic_chart, name='lect-CriticC'),
    path('estu-anio/', views.est_anio, name='estu-anio'),
    path('estu-edad/', views.est_edad, name='estu-edad'),
    path('desemp-ciu-edad/', views.desemp_ciu_edad, name='desemp-ciu-edad'),
    path('global-mun-ano/', views.global_mun_ano, name='global-mun-ano'),
    path('num-mun-ano/', viewsCubos.num_mun_ano, name='num-mun-ano'),
    path('grafic/', views.grafic, name='grafic'),
    path('subir/', views.subir, name='subir'),
    path('general/', viewsGeneral.generalDashboard, name='generalDashboard'),
    path('general-dashboard/', viewsGeneral.Dashboard, name='Dashboard'),
    path('genero-anio/', viewsCubos.generoAno, name='genero-anio'),
    # path('grafic/Dashboard/prueba.html', views.prueba)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='Dashboard/password_reset.html', email_template_name='Dashboard/password_reset_email.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='Dashboard/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Dashboard/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Dashboard/password_reset_done.html'), name='password_reset_complete'),

]

# urlpatterns += staticfiles_urlpatterns()
#
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
