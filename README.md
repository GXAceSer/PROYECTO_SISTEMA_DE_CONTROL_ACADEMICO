# PROYECTO_SISTEMA_DE_CONTROL_ACADEMICO

## Descripcion
Este proyecto consiste en un sistema de gestión escolar desarrollado en **Python** con conexion a **SQL SERVER**, que permite administrar alumnos, asignaturas y calificaciones. 
El sistema implementa operaciones CRUD, consultas con **JOINS**, cálculo de promedios y reportes.

## Objetivo
Este sistema resuleve el problema de la desorganizacion en el manejo de información academica, permitiendo registrar, consultar y gestionar alumnos, materias y calificciones de manera eficiente. 

## Tecnologiías utilizadas
- Python
- SQL Server
- pyodbc
- python-dotenv
- Lucidchart


## Base de datos
El sistema utiliza una base de datos relaconal con las siguientes tablas:
- Alumno
- Asignatura
- Cursa (relacion entre alumno y asignatura, donde contiene la calificación)

## Diagramas
Se realizaron los diagramas para el diseño del sistema:
- Diagrama entidad-relacion.
- Diagrama lógico.

## Funcionalidades
### Alumnos
- Registrar alumno.
- Mostrar alumnos.
- Editar alumno.
- Eliminar alumno.

### Asignaturas
- Registrar asignatura.
- Mostrar asignaturas.
  
### Calificaciones
- Asignar calificación.
- Consultar calificaciones:
  - Todas por alumno.
  - Por asignatura específica.
- Modificar calificación.
  
### Reportes 
- Promedio por alumno.
- Promedio por asignatura.
- Estado del alumno (Aprovado / Reprobado)

## Consultas SQL utilizadas
- JOIN
- AVG()
- COUNT()
- WHERE

## Procedimientos almacenados
Se implementaron procedimientos almacenados para mejorar la reutilización y seguridad:
- sp_InsertarAlumno
- sp_ConsultarAlumnos

## Configuración de entorno 
El proyecto utiliza un archivo .env para manejar las cedrenciales de la base de datos. 
Crea tu archivo .env en base al archivo de ejemplo **env.ejemplo**

## Ejecución del proyecto 
1. Clonar el repositorio.
2. Crear el archivo .env
3. Instalar dependencias:
```bash
pip install pyodbc python-dotenv
```
4. Ejecutar el programa:
```bash
python src/conexionBase.py
```

## Notas importantes
- Se utiliza ON DELETE CASCADE para mantener la integridad referencial.
- Al igual que cuenta con validaciones en python para evitar datos incorrectos.
- Y se tiene manejo de errores en conexion y consultas.

## Autor
## Acevedo Serrano Graciela Ximena. 
Proyecto desarrollado con fin de práctica académica y preparación para procesos de seleccion en desarrollo de software. 
