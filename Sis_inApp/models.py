from django.db import models
from django.contrib.auth.models import User

#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------

class Alertas(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey('Alumnos', models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    tipo = models.CharField(max_length=17, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    leida = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alertas'


class Alumnos(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    numero_control = models.CharField(max_length=20, blank=True, null=True)
    id_grupo = models.IntegerField(blank=True, null=True, db_column='id_grupo')  # Corregido a id_grupo
    user_id = models.IntegerField(blank=True, null=True, db_column='user_id')

    class Meta:
        managed = False
        db_table = 'alumnos'


class Asignaturas(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    id_carrera = models.ForeignKey('Carreras', models.DO_NOTHING, db_column='id_carrera', blank=True, null=True)
    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField(blank=True, null=True)
    horas_semana = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignaturas'


class Asistencias(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumnos, models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    id_horario = models.ForeignKey('Horarios', models.DO_NOTHING, db_column='id_horario', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    presente = models.IntegerField(blank=True, null=True)
    justificante = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asistencias'


class Calificaciones(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumnos, models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    id_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='id_asignatura', blank=True, null=True)
    calificacion = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    periodo = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calificaciones'


class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    perfil_egreso = models.TextField(blank=True, null=True)
    plan_estudios_documento = models.TextField(blank=True, null=True)
    mapa_curricular = models.TextField(blank=True, null=True)
    vigente = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carreras'


class Docentes(models.Model):
    id_docente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    numero_trabajador = models.CharField(max_length=20, blank=True, null=True)
    disponibilidad = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True, db_column='user_id')
    
    class Meta:
        managed = False
        db_table = 'docentes'


class Grupos(models.Model):
    id_grupo = models.AutoField(primary_key=True, db_column='id_grupo')  # Corregido a id_grupo
    id_carrera = models.ForeignKey(Carreras, models.DO_NOTHING, db_column='id_carrera', blank=True, null=True)
    nombre_grupo = models.CharField(max_length=50, blank=True, null=True, db_column='nombre_grupo')  # Corregido a nombre_grupo
    semestre = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupos'


class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    id_grupo = models.ForeignKey(Grupos, models.DO_NOTHING, db_column='id_grupo', blank=True, null=True)  # Corregido a id_grupo
    id_asignatura = models.ForeignKey(Asignaturas, models.DO_NOTHING, db_column='id_asignatura', blank=True, null=True)
    id_docente = models.ForeignKey(Docentes, models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    dia_semana = models.CharField(max_length=9, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horarios'
#------------------ZONA DE "Administracion_academica"-----------------------------------------------------------------------
# ...existing code...
class AsistenciasDocentes(models.Model):
    id_asistencia_docente = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docentes', models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    id_horario = models.ForeignKey('Horarios', models.DO_NOTHING, db_column='id_horario', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    presente = models.IntegerField(blank=True, null=True)
    justificacion = models.TextField(blank=True, null=True)
    hora_llegada = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asistencias_docentes'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Avisos(models.Model):
    id_aviso = models.AutoField(primary_key=True)
    id_autor = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_autor', blank=True, null=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    fecha_expiracion = models.DateField(blank=True, null=True)
    destinatarios = models.CharField(max_length=16, blank=True, null=True)
    id_grupo_destino = models.ForeignKey('Grupos', models.DO_NOTHING, db_column='id_grupo_destino', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avisos'


class Becas(models.Model):
    id_beca = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey('Alumnos', models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    tipo_beca = models.CharField(max_length=9, blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'becas'


class CargasDocentes(models.Model):
    id_carga = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docentes', models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    id_asignatura = models.ForeignKey('Asignaturas', models.DO_NOTHING, db_column='id_asignatura', blank=True, null=True)
    id_grupo = models.ForeignKey('Grupos', models.DO_NOTHING, db_column='id_grupo', blank=True, null=True)
    horas_semana = models.IntegerField(blank=True, null=True)
    ciclo_escolar = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargas_docentes'


class ConceptosPago(models.Model):
    id_concepto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    periodicidad = models.CharField(max_length=9, blank=True, null=True)
    obligatorio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conceptos_pago'


class DatosIndicadores(models.Model):
    id_dato_indicador = models.AutoField(primary_key=True)
    id_indicador = models.ForeignKey('Indicadores', models.DO_NOTHING, db_column='id_indicador', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_calculo = models.DateField(blank=True, null=True)
    ciclo_escolar = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos_indicadores'


class DisponibilidadDocentes(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docentes', models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    dia_semana = models.CharField(max_length=9, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disponibilidad_docentes'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DocumentosAlumnos(models.Model):
    id_documento = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey('Alumnos', models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    tipo_documento = models.CharField(max_length=15, blank=True, null=True)
    nombre_documento = models.CharField(max_length=255, blank=True, null=True)
    archivo = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentos_alumnos'


class EstadosCuenta(models.Model):
    id_estado_cuenta = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey('Alumnos', models.DO_NOTHING, db_column='id_alumno', blank=True, null=True)
    fecha_generacion = models.DateField(blank=True, null=True)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estatus = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados_cuenta'


class EvaluacionesDocentes(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docentes', models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    id_evaluador = models.IntegerField(blank=True, null=True)
    tipo_evaluacion = models.CharField(max_length=20, blank=True, null=True)
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    fecha_evaluacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluaciones_docentes'


class EventosCalendario(models.Model):
    id_evento = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    tipo_evento = models.CharField(max_length=14, blank=True, null=True)
    destinatarios = models.CharField(max_length=8, blank=True, null=True)
    id_autor = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_autor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos_calendario'


class Indicadores(models.Model):
    id_indicador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    formula_calculo = models.TextField(blank=True, null=True)
    periodicidad = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicadores'


class MaterialesBiblioteca(models.Model):
    id_material = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True, null=True)
    tipo_material = models.CharField(max_length=11, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    editorial = models.CharField(max_length=255, blank=True, null=True)
    año_publicacion = models.IntegerField(blank=True, null=True)
    ejemplares_disponibles = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materiales_biblioteca'


class Mensajes(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    id_remitente = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_remitente', blank=True, null=True)
    id_destinatario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_destinatario', related_name='mensajes_id_destinatario_set', blank=True, null=True)
    asunto = models.CharField(max_length=255, blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    leido = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mensajes'


class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_estado_cuenta = models.ForeignKey(EstadosCuenta, models.DO_NOTHING, db_column='id_estado_cuenta', blank=True, null=True)
    id_concepto = models.ForeignKey(ConceptosPago, models.DO_NOTHING, db_column='id_concepto', blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=13, blank=True, null=True)
    referencia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagos'


class Prestamos(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_material = models.ForeignKey(MaterialesBiblioteca, models.DO_NOTHING, db_column='id_material', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    fecha_prestamo = models.DateField(blank=True, null=True)
    fecha_devolucion_esperada = models.DateField(blank=True, null=True)
    fecha_devolucion_real = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=8, blank=True, null=True)
    multa = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestamos'


class ReportesEstadisticos(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    tipo_reporte = models.CharField(max_length=19, blank=True, null=True)
    fecha_generacion = models.DateTimeField(blank=True, null=True)
    parametros = models.JSONField(blank=True, null=True)
    datos = models.JSONField(blank=True, null=True)
    id_usuario_generador = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_generador', blank=True, null=True)        

    class Meta:
        managed = False
        db_table = 'reportes_estadisticos'


class Reservaciones(models.Model):
    id_reservacion = models.AutoField(primary_key=True)
    id_material = models.ForeignKey(MaterialesBiblioteca, models.DO_NOTHING, db_column='id_material', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    fecha_reservacion = models.DateTimeField(blank=True, null=True)
    fecha_vencimiento_reserva = models.DateField(blank=True, null=True)
    estatus = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservaciones'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_persona = models.IntegerField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=14, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
# ...existing code...
