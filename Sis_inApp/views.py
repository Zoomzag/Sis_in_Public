from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Carreras, Grupos, Alumnos, Docentes, Asignaturas, Horarios, Calificaciones, Asistencias, Alertas
from django.db.models import Count, Avg, Q
from django.db import connection
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Becas, Pagos, EstadosCuenta, Usuarios


def _missing_model_tables(*model_classes):
    existing_tables = set(connection.introspection.table_names())
    return [
        model._meta.db_table
        for model in model_classes
        if model._meta.db_table not in existing_tables
    ]

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # SOLUCIÓN SIMPLE - Solo por formato del username
            if username.startswith('2'):
                return redirect('indexA')
            elif username.startswith('9'):
                return redirect('index')
            else:
                return redirect('index')
        else:
            return render(request, 'log_in.html', {'form': {'errors': True}})
    
    return render(request, 'log_in.html')

def index(request):
    return render(request,'index.html', {})

def indexA(request):
    return render(request,'indexA.html', {})
def Modulo_1(request):
    return render(request, 'Modulo_1/base.html', {'active_page': 'dashboard'})

def Modulo_2(request):
    return render(request, 'Modulo_2/index.html')

def Modulo_3(request):
    return render(request, 'Modulo_3/index.html')

def Modulo_4(request):
    return render(request, 'Modulo_4/index.html')

def Modulo_5(request):
    return render(request, 'Modulo_5/index.html')

def Modulo_6(request):
    return redirect('biblioteca')

def Modulo_7(request):
    total_alumnos = Alumnos.objects.count()
    total_grupos = Grupos.objects.count()
    total_calificaciones = Calificaciones.objects.count()
    total_asistencias = Asistencias.objects.count()
    presentes = Asistencias.objects.filter(presente=True).count()
    promedio = Calificaciones.objects.aggregate(promedio=Avg('calificacion'))['promedio']
    porcentaje_asistencia = (presentes / total_asistencias * 100) if total_asistencias else 0
    calificaciones_recientes = Calificaciones.objects.select_related(
        'id_alumno', 'id_asignatura'
    ).order_by('-id_calificacion')[:8]

    context = {
        'total_alumnos': total_alumnos,
        'total_grupos': total_grupos,
        'total_calificaciones': total_calificaciones,
        'total_asistencias': total_asistencias,
        'porcentaje_asistencia': round(porcentaje_asistencia, 1),
        'promedio_calificacion': round(float(promedio), 1) if promedio is not None else 0,
        'calificaciones_recientes': calificaciones_recientes,
    }
    return render(request, 'Modulo_7/index.html', context)

#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------

def base(request):
    return render(request, 'Modulo_1/base.html', {'active_page': 'dashboard'})

def dashboard(request):
   
    planes_count = Carreras.objects.count()
    estudiantes_count = Alumnos.objects.count()
    docentes_count = Docentes.objects.count()
    grupos_count = Grupos.objects.count()

    alertas_recientes = Alertas.objects.filter(leida=False).order_by('-fecha')[:5]
    
    actividades = [
        {'fecha': timezone.now().date(), 'descripcion': 'Sistema de administración académica iniciado'},
        {'fecha': timezone.now().date(), 'descripcion': f'{estudiantes_count} estudiantes registrados'},
        {'fecha': timezone.now().date(), 'descripcion': f'{docentes_count} docentes activos'},
    ]
    
    context = {
        'planes_count': planes_count,
        'estudiantes_count': estudiantes_count,
        'docentes_count': docentes_count,
        'grupos_count': grupos_count,
        'alertas': alertas_recientes,
        'actividades': actividades,
        'active_page': 'dashboard'
    }
    return render(request, 'Modulo_1/dashboard.html', context)

def gestion_planes(request):
  
    planes = Carreras.objects.all()
    
    
    procesos = [
        {
            'entrada': 'Requisitos normativos',
            'salida': 'Plan de estudios', 
            'justificacion': 'Se genera un documento que contiene toda la información respecto a la carrera'
        },
        {
            'entrada': 'Perfil de egreso',
            'salida': 'Mapa curricular', 
            'justificacion': 'Se genera una representación visual del plan de estudios'
        },
        {
            'entrada': 'Propuesta académica',
            'salida': 'Catalogo de asignaturas', 
            'justificacion': 'Se genera una lista de todas las asignaturas disponibles, así como sus horarios'
        },
    ]
    
    context = {
        'procesos': procesos,
        'planes': planes,
        'active_page': 'gestion'
    }
    return render(request, 'Modulo_1/gestion_planes.html', context)

def control_horarios(request):
   
    grupos = Grupos.objects.select_related('id_carrera').all()
    
  
    docentes = Docentes.objects.annotate(
        num_asignaturas=Count('horarios__id_asignatura', distinct=True)
    )
    
    horarios = Horarios.objects.select_related(
        'id_grupo', 'id_asignatura', 'id_docente'
    )[:10]  
    
    context = {
        'grupos': grupos,
        'docentes': docentes,
        'horarios': horarios,
        'active_page': 'control'
    }
    return render(request, 'Modulo_1/control_horarios.html', context)

def evaluaciones(request):
    
    grupos = Grupos.objects.select_related('id_carrera').all()
    
  
    asignaturas = Asignaturas.objects.select_related('id_carrera').all()
   
    alertas_riesgo = Alertas.objects.filter(
        tipo='Baja calificación', 
        leida=False
    ).select_related('id_alumno')[:5]
 
    calificaciones_recientes = Calificaciones.objects.select_related(
        'id_alumno', 'id_asignatura'
    ).order_by('-id_calificacion')[:5]
    
    context = {
        'grupos': grupos,
        'asignaturas': asignaturas,
        'alertas_riesgo': alertas_riesgo,
        'calificaciones_recientes': calificaciones_recientes,
        'active_page': 'evaluaciones'
    }
    return render(request, 'Modulo_1/evaluaciones.html', context)

def control_asistencia(request):
    
    grupos = Grupos.objects.select_related('id_carrera').all()
    

    asignaturas = Asignaturas.objects.select_related('id_carrera').all()

    alertas_inasistencia = Alertas.objects.filter(
        tipo='Inasistencias', 
        leida=False
    ).select_related('id_alumno')[:5]
    
 
    asistencias_recientes = Asistencias.objects.select_related(
        'id_alumno', 'id_horario'
    ).order_by('-fecha')[:5]
    
    
    total_asistencias = Asistencias.objects.count()
    total_presentes = Asistencias.objects.filter(presente=True).count()
    porcentaje_asistencia = (total_presentes / total_asistencias * 100) if total_asistencias > 0 else 0
    
    context = {
        'grupos': grupos,
        'asignaturas': asignaturas,
        'alertas_inasistencia': alertas_inasistencia,
        'asistencias_recientes': asistencias_recientes,
        'porcentaje_asistencia': round(porcentaje_asistencia, 2),
        'active_page': 'asistencia'
    }
    return render(request, 'Modulo_1/control_asistencia.html', context)
#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------
#------------------ZONA DE "LOG_OUT"-----------------------------------------------------------------------------------------
def log_out(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('log_in')
#------------------ZONA DE "LOG_OUT"-----------------------------------------------------------------------------------------
#------------------ZONA DE "SEGURIDAD"---------------------------------------------------------------------------------------
#------------------ZONA DE "SEGURIDAD"---------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required

# Vista genérica para agregar elementos
@login_required
def agregar_elemento(request, modelo):
    """
    Vista genérica para agregar cualquier elemento
    """
    if request.user.is_staff:
        urls_admin = {
            'carrera': '/admin/Sis_inApp/carreras/add/',
            'asignatura': '/admin/Sis_inApp/asignaturas/add/',
            'grupo': '/admin/Sis_inApp/grupos/add/',
            'docente': '/admin/Sis_inApp/docentes/add/',
            'alumno': '/admin/Sis_inApp/alumnos/add/',
            'horario': '/admin/Sis_inApp/horarios/add/',
            'calificacion': '/admin/Sis_inApp/calificaciones/add/',
            'asistencia': '/admin/Sis_inApp/asistencias/add/',
        }
        return redirect(urls_admin.get(modelo, '/admin/'))
    else:
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect('dashboard')

# Vistas específicas para cada modelo
@login_required
def agregar_carrera(request):
    return agregar_elemento(request, 'carrera')

@login_required
def agregar_asignatura(request):
    return agregar_elemento(request, 'asignatura')

@login_required
def agregar_grupo(request):
    return agregar_elemento(request, 'grupo')

@login_required
def agregar_docente(request):
    return agregar_elemento(request, 'docente')

@login_required
def agregar_alumno(request):
    return agregar_elemento(request, 'alumno')

@login_required
def agregar_horario(request):
    return agregar_elemento(request, 'horario')

@login_required
def agregar_calificacion(request):
    return agregar_elemento(request, 'calificacion')

@login_required
def agregar_asistencia(request):
    return agregar_elemento(request, 'asistencia')
#------------------ZONA DE "SEGURIDAD"---------------------------------------------------------------------------------------
#------------------ZONA DE "GESTION ALUMNOS"-------------------------------------------------------------------------------
def dashboard2(request):
    # Estadísticas para el dashboard
    total_alumnos = Alumnos.objects.count()
    grupos_count = Grupos.objects.count()
    
    context = {
        'total_alumnos': total_alumnos,
        'grupos_count': grupos_count,
        'active_page': 'dashboard_alumnos'
    }
    return render(request, 'Gestion_de_Alumnos/dashboard2.html', context)

# API para obtener alumnos
def obtener_alumnos(request):
    try:
        alumnos = Alumnos.objects.select_related('id_grupo').all()
        alumnos_data = []
        
        for alumno in alumnos:
            alumnos_data.append({
                'id_alumno': alumno.id_alumno,
                'nombre': alumno.nombre,
                'grupo_nombre': alumno.id_grupo.nombre_grupo if alumno.id_grupo else 'Sin grupo',
                'id_grupo': alumno.id_grupo_id
            })
        
        return JsonResponse(alumnos_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API para obtener grupos
def obtener_grupos(request):
    try:
        grupos = Grupos.objects.all().values('id_grupo', 'nombre_grupo', 'semestre')
        return JsonResponse(list(grupos), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API para inscripción de alumnos
@csrf_exempt
def inscripcion_alumno(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            grupo_id = data.get('id_grupo') or None

            if not nombre:
                return JsonResponse(
                    {'success': False, 'message': 'El nombre del alumno es requerido'},
                    status=400,
                )
            if grupo_id and not Grupos.objects.filter(id_grupo=grupo_id).exists():
                return JsonResponse(
                    {'success': False, 'message': 'El grupo seleccionado no existe'},
                    status=400,
                )

            alumno = Alumnos.objects.create(
                nombre=nombre,
                id_grupo_id=grupo_id,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Alumno inscrito correctamente',
                'id': alumno.id_alumno,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

# API para reinscripción
@csrf_exempt
def reinscripcion_alumno(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alumno_id = data.get('alumno_id')
            nuevo_grupo = data.get('nuevo_grupo')

            if not nuevo_grupo or not Grupos.objects.filter(id_grupo=nuevo_grupo).exists():
                return JsonResponse(
                    {'success': False, 'message': 'El grupo seleccionado no existe'},
                    status=400,
                )

            alumno = Alumnos.objects.get(id_alumno=alumno_id)
            alumno.id_grupo_id = nuevo_grupo
            alumno.save(update_fields=['id_grupo'])
            
            return JsonResponse({'success': True, 'message': 'Reinscripción exitosa'})
        except Alumnos.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Alumno no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

# API para expediente de alumnos
def expediente_alumno(request, alumno_id):
    try:
        alumno = Alumnos.objects.select_related('id_grupo').get(id_alumno=alumno_id)
        grupo_nombre = alumno.id_grupo.nombre_grupo if alumno.id_grupo else 'Sin grupo'
        
        # Obtener calificaciones
        calificaciones = Calificaciones.objects.filter(id_alumno=alumno_id).select_related('id_asignatura')
        calificaciones_data = []
        for cal in calificaciones:
            calificaciones_data.append({
                'asignatura': cal.id_asignatura.nombre if cal.id_asignatura else 'N/A',
                'calificacion': float(cal.calificacion) if cal.calificacion else None,
                'periodo': cal.periodo,
                'observaciones': cal.observaciones
            })
        
        # Obtener asistencias
        asistencias = Asistencias.objects.filter(id_alumno=alumno_id).select_related('id_horario__id_asignatura')
        asistencias_data = []
        for asist in asistencias:
            asistencias_data.append({
                'fecha': asist.fecha.strftime('%Y-%m-%d') if asist.fecha else None,
                'presente': bool(asist.presente),
                'asignatura': asist.id_horario.id_asignatura.nombre if asist.id_horario and asist.id_horario.id_asignatura else 'N/A'
            })
        
        data = {
            'alumno': {
                'id': alumno.id_alumno,
                'nombre': alumno.nombre,
                'grupo': grupo_nombre
            },
            'calificaciones': calificaciones_data,
            'asistencias': asistencias_data
        }
        
        return JsonResponse(data)
    except Alumnos.DoesNotExist:
        return JsonResponse({'error': 'Alumno no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API para reportes
def generar_reporte(request, tipo_reporte):
    try:
        if tipo_reporte == 'alumnos':
            data = list(Alumnos.objects.all().values(
                'id_alumno', 'nombre', 'id_grupo'
            )[:50])
        elif tipo_reporte == 'calificaciones':
            data = list(Calificaciones.objects.select_related('id_alumno', 'id_asignatura').values(
                'id_alumno__nombre', 'id_asignatura__nombre', 'calificacion', 'periodo'
            )[:50])
        elif tipo_reporte == 'asistencias':
            data = list(Asistencias.objects.select_related('id_alumno').values(
                'id_alumno__nombre', 'fecha', 'presente'
            )[:50])
        else:
            data = []
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#------------------ZONA DE "GESTION ALUMNOS"-------------------------------------------------------------------------------
#------------------ZONA DE "GESTION DE DOCENTES"-------------------------------------------------------------------------------
from django.contrib import messages
from django.db import IntegrityError
from .models import Docentes, Asignaturas, Grupos, Horarios, EvaluacionesDocentes


def gestion_docentes(request):
    """
    Vista principal de gestión docente. Muestra docentes, asignaturas, grupos y horarios actuales.
    """
    contexto = {
        'docentes': Docentes.objects.all(),
        'asignaturas': Asignaturas.objects.all(),
        'grupos': Grupos.objects.all(),
        'horarios': Horarios.objects.select_related('id_docente', 'id_asignatura', 'id_grupo').all(),
        'active_page': 'docentes'
    }
    # Ruta correcta de la plantilla dentro de templates/Gestion_Docente/
    return render(request, 'Gestion_Docente/gestion_docentes.html', contexto)


def asignar_grupo(request):
    """
    Asigna una materia y grupo a un docente creando un registro en la tabla Horarios.
    """
    if request.method == 'POST':
        try:
            Horarios.objects.create(
                id_docente_id=request.POST['id_docente'],
                id_asignatura_id=request.POST['id_asignatura'],
                id_grupo_id=request.POST['id_grupo'],
                dia_semana='Lunes',  # Valor por defecto; editable después
                hora_inicio='08:00:00',
                hora_fin='09:00:00'
            )
            messages.success(request, "Asignación creada correctamente.")
        except IntegrityError:
            messages.error(request, "Error: los datos de asignación no son válidos.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

    # Redirige usando el nombre de la vista, no una ruta literal
    return redirect('gestion_docentes')


def evaluar_docente(request):
    """
    Permite registrar evaluaciones de desempeño para los docentes.
    """
    if request.method == 'POST':
        try:
            EvaluacionesDocentes.objects.create(
                id_docente_id=request.POST['id_docente'],
                tipo_evaluacion=request.POST['tipo_evaluacion'],
                puntuacion=request.POST['puntuacion'],
                comentarios=request.POST.get('comentarios', ''),
                fecha_evaluacion=request.POST.get('fecha_evaluacion') or timezone.localdate(),
                id_evaluador=request.user.pk if request.user.is_authenticated else None,
            )
            messages.success(request, "Evaluación guardada correctamente.")
        except IntegrityError:
            messages.error(request, "Error al guardar la evaluación (revisa los datos).")
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

    return redirect('gestion_docentes')
#------------------FIN DE "GESTION DE DOCENTES"-------------------------------------------------------------------------------
#------------------ZONA DE "CONTROL FINANCIERO"-------------------------------------------------------------------------------
def control_financiero(request):
    """
    Vista para el control administrativo y financiero
    """
    # Obtener datos para mostrar en el dashboard
    total_alumnos = Alumnos.objects.count()
    missing_tables = _missing_model_tables(Becas, Pagos, EstadosCuenta)
    if missing_tables:
        total_becas = total_pagos = estados_pendientes = None
    else:
        total_becas = Becas.objects.count()
        total_pagos = Pagos.objects.count()
        estados_pendientes = EstadosCuenta.objects.filter(estatus='Pendiente').count()
    
    context = {
        'active_page': 'financiero',
        'total_alumnos': total_alumnos,
        'total_becas': total_becas,
        'total_pagos': total_pagos,
        'estados_pendientes': estados_pendientes,
        'financial_data_available': not missing_tables,
        'missing_financial_tables': missing_tables,
    }
    return render(request, 'Control_Admi_fina/financieros.html', context)
#------------------ZONA DE "CONTROL FINANCIERO"-------------------------------------------------------------------------------
from django.utils import timezone
from .models import MaterialesBiblioteca, Prestamos
#------------------ZONA DE "CONTROL FINANCIERO"-------------------------------------------------------------------------------
#------------------ZONA DE "BIBLIOTECA"-------------------------------------------------------------------------------
def biblioteca(request):
    """
    Vista para el módulo de biblioteca
    """
    missing_tables = _missing_model_tables(MaterialesBiblioteca, Prestamos, Usuarios)
    if missing_tables:
        materiales_count = prestamos_activos = prestamos_vencidos = recursos_digitales = None
        prestamos_activos_list = materiales = recursos_digitales_list = []
    else:
        materiales_count = MaterialesBiblioteca.objects.count()
        prestamos_activos = Prestamos.objects.filter(estatus='Activo').count()
        prestamos_vencidos = Prestamos.objects.filter(
            estatus='Activo',
            fecha_devolucion_esperada__lt=timezone.localdate(),
        ).count()
        recursos_digitales = MaterialesBiblioteca.objects.filter(
            tipo_material__in=['e-Book', 'Video', 'Audio', 'Software']
        ).count()
        prestamos_activos_list = Prestamos.objects.filter(estatus='Activo').select_related(
            'id_material', 'id_usuario'
        )[:10]

        categoria = request.GET.get('categoria', '')
        if categoria == 'libros':
            materiales = MaterialesBiblioteca.objects.filter(tipo_material='Libro')[:20]
        elif categoria == 'revistas':
            materiales = MaterialesBiblioteca.objects.filter(tipo_material='Revista')[:20]
        elif categoria == 'tesis':
            materiales = MaterialesBiblioteca.objects.filter(tipo_material='Tesis')[:20]
        elif categoria == 'audiovisual':
            materiales = MaterialesBiblioteca.objects.filter(tipo_material='Video')[:20]
        elif categoria == 'digitales':
            materiales = MaterialesBiblioteca.objects.filter(
                tipo_material__in=['e-Book', 'Software']
            )[:20]
        else:
            materiales = MaterialesBiblioteca.objects.all()[:20]

        recursos_digitales_list = MaterialesBiblioteca.objects.filter(
            tipo_material__in=['e-Book', 'Video', 'Audio', 'Software']
        )[:9]
    
    context = {
        'active_page': 'biblioteca',
        'materiales_count': materiales_count,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': prestamos_vencidos,
        'recursos_digitales': recursos_digitales,
        'prestamos_activos_list': prestamos_activos_list,
        'materiales': materiales,
        'recursos_digitales_list': recursos_digitales_list,
        'now': timezone.localdate(),
        'library_data_available': not missing_tables,
        'missing_library_tables': missing_tables,
    }
    return render(request, 'Biblioteca/biblioteca.html', context)

@login_required
def registrar_prestamo(request):
    """
    Vista para registrar un nuevo préstamo
    """
    if request.method == 'POST':
        messages.error(request, "El registro de préstamos no está habilitado en este sistema.")
    
    return redirect('biblioteca')

@login_required
def registrar_devolucion(request):
    """
    Vista para registrar una devolución
    """
    if request.method == 'POST':
        messages.error(request, "El registro de devoluciones no está habilitado en este sistema.")
    
    return redirect('biblioteca')

@login_required
def ver_material(request, material_id):
    """
    Vista para ver detalles de un material
    """
    if _missing_model_tables(MaterialesBiblioteca):
        messages.error(request, "El catálogo de biblioteca no está configurado.")
        return redirect('biblioteca')

    try:
        material = MaterialesBiblioteca.objects.get(id_material=material_id)
        context = {
            'material': material,
            'active_page': 'biblioteca'
        }
        return render(request, 'Biblioteca/ver_material.html', context)
    except MaterialesBiblioteca.DoesNotExist:
        messages.error(request, "Material no encontrado")
        return redirect('biblioteca')

@login_required
def editar_material(request, material_id):
    """
    Vista para editar un material
    """
    if _missing_model_tables(MaterialesBiblioteca):
        messages.error(request, "El catálogo de biblioteca no está configurado.")
        return redirect('biblioteca')

    try:
        material = MaterialesBiblioteca.objects.get(id_material=material_id)
        
        if request.method == 'POST':
            messages.error(request, "La edición de materiales todavía no está habilitada.")
            return redirect('biblioteca')
        
        context = {
            'material': material,
            'active_page': 'biblioteca'
        }
        return render(request, 'Biblioteca/editar_material.html', context)
    except MaterialesBiblioteca.DoesNotExist:
        messages.error(request, "Material no encontrado")
        return redirect('biblioteca')

@login_required
def acceder_recurso(request, recurso_id):
    """
    Vista para acceder a un recurso digital
    """
    messages.error(request, "El acceso a recursos digitales no está configurado.")
    return redirect('biblioteca')
#------------------ZONA DE "BIBLIOTECA"-------------------------------------------------------------------------------
#------------------ZONA DE "EXTRAS"-------------------------------------------------------------------------------
def tramites(request):
    return render(request, 'Extras/tramites.html', {'active_page': 'tramites'})

def eva_docente(request):
    return render(request, 'Extras/eva_docente.html', {'active_page': 'eva_docente'})

def act_extra(request):
    return render(request, 'Extras/act_extra.html', {'active_page': 'act_extra'})

#------------------ZONA DE "EXTRAS"-------------------------------------------------------------------------------
