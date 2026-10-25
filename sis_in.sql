create database Sis_in;
use Sis_in;

-- Tabla: Carreras
CREATE TABLE Carreras (
    id_carrera INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    perfil_egreso TEXT,
    plan_estudios_documento BLOB,
    mapa_curricular BLOB,
    vigente BOOLEAN DEFAULT TRUE
);

-- Tabla: Asignaturas
CREATE TABLE Asignaturas (
    id_asignatura INT PRIMARY KEY AUTO_INCREMENT,
    id_carrera INT,
    nombre VARCHAR(255) NOT NULL,
    creditos INT,
    horas_semana INT,
    FOREIGN KEY (id_carrera) REFERENCES Carreras(id_carrera)
);

-- Tabla: Docentes
CREATE TABLE Docentes (
    id_docente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    disponibilidad TEXT -- JSON o texto con horarios disponibles
);

-- Tabla: Grupos
CREATE TABLE Grupos (
    id_grupo INT PRIMARY KEY AUTO_INCREMENT,
    id_carrera INT,
    nombre_grupo VARCHAR(50),
    semestre INT,
    FOREIGN KEY (id_carrera) REFERENCES Carreras(id_carrera)
);

-- Tabla: Horarios
CREATE TABLE Horarios (
    id_horario INT PRIMARY KEY AUTO_INCREMENT,
    id_grupo INT,
    id_asignatura INT,
    id_docente INT,
    dia_semana ENUM('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'),
    hora_inicio TIME,
    hora_fin TIME,
    FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo),
    FOREIGN KEY (id_asignatura) REFERENCES Asignaturas(id_asignatura),
    FOREIGN KEY (id_docente) REFERENCES Docentes(id_docente)
);

-- Tabla: Alumnos
CREATE TABLE Alumnos (
    id_alumno INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    id_grupo INT,
    FOREIGN KEY (id_grupo) REFERENCES Grupos(id_grupo)
);

-- Tabla: Calificaciones
CREATE TABLE Calificaciones (
    id_calificacion INT PRIMARY KEY AUTO_INCREMENT,
    id_alumno INT,
    id_asignatura INT,
    calificacion DECIMAL(4,2),
    periodo VARCHAR(50), -- e.g., "2025-1", "Parcial 1"
    observaciones TEXT,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno),
    FOREIGN KEY (id_asignatura) REFERENCES Asignaturas(id_asignatura)
);

-- Tabla: Asistencias
CREATE TABLE Asistencias (
    id_asistencia INT PRIMARY KEY AUTO_INCREMENT,
    id_alumno INT,
    id_horario INT,
    fecha DATE,
    presente BOOLEAN DEFAULT FALSE,
    justificante TEXT,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno),
    FOREIGN KEY (id_horario) REFERENCES Horarios(id_horario)
);

-- Tabla: Alertas
CREATE TABLE Alertas (
    id_alerta INT PRIMARY KEY AUTO_INCREMENT,
    id_alumno INT,
    tipo ENUM('Baja calificación', 'Inasistencias', 'Riesgo académico'),
    mensaje TEXT,
    fecha DATE,
    leida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno)
);

