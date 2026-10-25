from django.contrib import admin
from .models import (
    Alertas, Alumnos, Asignaturas, Asistencias, Calificaciones,
    Carreras, Docentes, Grupos, Horarios
)

admin.site.register(Alertas)
admin.site.register(Alumnos)
admin.site.register(Asignaturas)
admin.site.register(Asistencias)
admin.site.register(Calificaciones)
admin.site.register(Carreras)
admin.site.register(Docentes)
admin.site.register(Grupos)
admin.site.register(Horarios)