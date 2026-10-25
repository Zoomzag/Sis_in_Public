```text
   _____ _     _                         _____       _                       _   _____           _   _ _              _                   _ 
  / ____(_)   | |                       |_   _|     | |                     | | |_   _|         | | (_) |            (_)                 | |
 | (___  _ ___| |_ ___ _ __ ___   __ _    | |  _ __ | |_ ___  __ _ _ __ __ _| |   | |  _ __  ___| |_ _| |_ _   _  ___ _  ___  _ __   __ _| |
  \___ \| / __| __/ _ \ '_ ` _ \ / _` |   | | | '_ \| __/ _ \/ _` | '__/ _` | |   | | | '_ \/ __| __| | __| | | |/ __| |/ _ \| '_ \ / _` | |
  ____) | \__ \ ||  __/ | | | | | (_| |  _| |_| | | | ||  __/ (_| | | | (_| | |  _| |_| | | \__ \ |_| | |_| |_| | (__| | (_) | | | | (_| | |
 |_____/|_|___/\__\___|_| |_| |_|\__,_| |_____|_| |_|\__\___|\__, |_|  \__,_|_| |_____|_| |_|___/\__|_|\__|\__,_|\___|_|\___/|_| |_|\__,_|_|
                                                              __/ |                                                                         
                                                             |___/                                                                          
```

# Sistema Integral Institucional

Es un sistema inspirado en el antiguo SII que usaba el Instituto Tecnológico de Chihuahua Campus II. La idea es tener en un solo lugar las cosas que necesitan el personal administrativo, los docentes y los alumnos.

Está hecho con **Python** y **Django**, y usa **MySQL** como base de datos. Todavía no está terminado.

## ¿Qué hace?

- **Inicio de sesión:** entras con tu usuario y, según el tipo de usuario, te manda a una pantalla u otra.
- **Administración académica:** ver las carreras, los horarios, las evaluaciones y la asistencia, con alertas cuando un alumno tiene baja calificación o muchas faltas.
- **Gestión de alumnos:** inscribir y reinscribir alumnos, ver su expediente (calificaciones y asistencias) y sacar reportes.
- **Gestión de docentes:** asignar materias y grupos a los docentes y evaluar su desempeño.
- **Control financiero:** becas, pagos y estados de cuenta.
- **Biblioteca:** catálogo de libros y materiales, préstamos y devoluciones.
- **Extras:** trámites, evaluación docente y actividades extra.

## ¿Cómo está organizado?

- `Sis_In/` → la configuración del proyecto.
- `Sis_inApp/` → el código principal: `models.py` (tablas), `views.py` (lo que hace cada pantalla) y `urls.py` (las direcciones).
- `Templates/` → las páginas HTML.
- `Static/` → CSS, JavaScript e imágenes.

## ¿Cómo lo corro?

1. Instala las librerías:

   ```bash
   pip install django mysqlclient
   ```

2. Crea la base de datos `sis_in` en MySQL con sus tablas. Django no las crea solo, tienen que existir antes.

3. Pon tu usuario y contraseña de MySQL en `Sis_In/settings.py`, en la parte de `DATABASES`.

4. Inicia el servidor:

   ```bash
   python manage.py runserver
   ```

5. Abre `http://127.0.0.1:8000/` en el navegador.
