from django.contrib import admin
from django.urls import path

from.import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.log_in, name='log_in'),
    path("index/", views.index, name='index'),
<<<<<<< HEAD
    path("indexA/", views.indexA, name='indexA'),
=======
    path("Modulo_1/", views.Modulo_1, name='Modulo_1'),
    path('Modulo_2/', views.Modulo_2, name='Modulo_2'),
    path('Modulo_3/', views.Modulo_3, name='Modulo_3'),
    path('Modulo_4/', views.Modulo_4, name='Modulo_4'),
    path('Modulo_5/', views.Modulo_5, name='Modulo_5'),
    path('Modulo_6/', views.Modulo_6, name='Modulo_6'),
    path('Modulo_7/', views.Modulo_7, name='Modulo_7'),
    
>>>>>>> e483321197913929d645ccd160a7fbb8850623b2
#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------
    path("base/", views.base, name='base'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("gestion_planes/", views.gestion_planes, name='gestion_planes'),
    path('control_horarios/', views.control_horarios, name='control_horarios'),
    path('evaluaciones/', views.evaluaciones, name='evaluaciones'),
    path('control_asistencia/', views.control_asistencia, name='control_asistencia'),
#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------
#------------------ZONA DE LOG_OUT"-----------------------------------------------------------------------------------------
    path('logout/', views.log_out, name='logout'),
#------------------ZONA DE "SEGURIDAD"---------------------------------------------------------------------------------------
    path('agregar-carrera/', views.agregar_carrera, name='agregar_carrera'),
    path('agregar-asignatura/', views.agregar_asignatura, name='agregar_asignatura'),
    path('agregar-grupo/', views.agregar_grupo, name='agregar_grupo'),
    path('agregar-docente/', views.agregar_docente, name='agregar_docente'),
    path('agregar-alumno/', views.agregar_alumno, name='agregar_alumno'),
     # Agrega estas URLs que faltan:
    path('agregar-horario/', views.agregar_horario, name='agregar_horario'),
    path('agregar-calificacion/', views.agregar_calificacion, name='agregar_calificacion'),
    path('agregar-asistencia/', views.agregar_asistencia, name='agregar_asistencia'),
#------------------ZONA DE "SEGURIDAD"---------------------------------------------------------------------------------------
#------------------ZONA DE "GESTION DE ALUMNOS"-------------------------------------------------------------------------------
path('dashboard2/', views.dashboard2, name='dashboard2'),

# APIs para Gestión de Alumnos
path('api/alumnos/', views.obtener_alumnos, name='obtener_alumnos'),
path('api/grupos/', views.obtener_grupos, name='obtener_grupos'),
path('api/inscripcion/', views.inscripcion_alumno, name='inscripcion_alumno'),
path('api/reinscripcion/', views.reinscripcion_alumno, name='reinscripcion_alumno'),
path('api/expediente/<int:alumno_id>/', views.expediente_alumno, name='expediente_alumno'),
path('api/reportes/<str:tipo_reporte>/', views.generar_reporte, name='generar_reporte'),

#------------------ZONA DE "GESTION ACADEMICA"-------------------------------------------------------------------------------
#------------------ZONA DE "GESTION DEOCENTES"-------------------------------------------------------------------------------
    path('gestion_docentes/', views.gestion_docentes, name='gestion_docentes'),
    path('asignar_grupo/', views.asignar_grupo, name='asignar_grupo'),
    path('evaluar_docente/', views.evaluar_docente, name='evaluar_docente'),
#------------------ZONA DE "GESTION DEOCENTES"-------------------------------------------------------------------------------
#------------------ZONA DE "CONTROL FINANCIERO"-------------------------------------------------------------------------------
path('control_financiero/', views.control_financiero, name='control_financiero'),
#------------------ZONA DE "CONTROL FINANCIERO"-------------------------------------------------------------------------------
#------------------ZONA DE "BIBLIOTECA"-------------------------------------------------------------------------------
path('biblioteca/', views.biblioteca, name='biblioteca'),
path('registrar-prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
path('registrar-devolucion/', views.registrar_devolucion, name='registrar_devolucion'),
path('ver-material/<int:material_id>/', views.ver_material, name='ver_material'),
path('editar-material/<int:material_id>/', views.editar_material, name='editar_material'),
path('acceder-recurso/<int:recurso_id>/', views.acceder_recurso, name='acceder_recurso'),
#------------------ZONA DE "BIBLIOTECA"-------------------------------------------------------------------------------
#------------------ZONA DE "EXTRAS"-------------------------------------------------------------------------------
path('tramites/', views.tramites, name='tramites'),
path('eva_docente/', views.eva_docente, name='eva_docente'),
path(' act_extra/', views.act_extra, name='act_extra'),
#------------------ZONA DE "EXTRAS"-------------------------------------------------------------------------------

]

