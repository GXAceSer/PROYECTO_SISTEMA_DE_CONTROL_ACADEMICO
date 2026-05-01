-------------------------------------------------
-- Autor: Graciela Ximena Acevedo Serrano --
-- Proyecto: Sistema de Gestión de Alumnos --
-- Descripción: Base de datos con gestion de alumnos, asignaturas y calificaciones--

USE ProyectAlumnos;

--Permite recrear la base de datos desde cero
--ESTO ES CON FINES DE DESARROLLO/PRUEBA
DROP TABLE IF EXISTS Cursa;
DROP TABLE IF EXISTS Alumno;
DROP TABLE IF EXISTS Asignatura;

GO

-- Tabla ALUMNO
CREATE TABLE Alumno(
noCuenta BIGINT PRIMARY KEY,
nombreAlum VARCHAR(30) NOT NULL,
apPatAlum VARCHAR(30) NOT NULL,
apMatAlum VARCHAR(30) NOT NULL,
edadAlum INT CHECK (edadAlum >= 0) NOT NULL --Se valida que la edad sea mayor a cero
);

--Tabla ASIGNATURA
CREATE TABLE Asignatura(
idAsign INT PRIMARY KEY,
nombreAsign VARCHAR(30) NOT NULL,
cupo NUMERIC(5) CHECK (cupo >= 0) NOT NULL, 
creditos NUMERIC(5) CHECK (creditos BETWEEN 1 AND 14) NOT NULL --Se valida que el valor de los creditos este entre los valores 1 y 14
);

--Tabla CURSA (RELACIÓN)
CREATE TABLE Cursa(
noCuenta BIGINT,
idAsign INT,
calificacion NUMERIC(4,2) CHECK (calificacion BETWEEN 0 AND 10),

PRIMARY KEY (noCuenta,idAsign),

FOREIGN KEY (noCuenta) REFERENCES Alumno(noCuenta) ON DELETE CASCADE,
FOREIGN KEY (idAsign) REFERENCES Asignatura(idAsign)
);

--Se insertan datos de prueba
INSERT INTO Asignatura VALUES (103, 'Matematicas', 30, 8);
INSERT INTO Asignatura VALUES (105, 'Programacion', 25, 10);
INSERT INTO Asignatura VALUES (201, 'Literatura', 30, 8);
INSERT INTO Asignatura VALUES (204, 'Redaccion', 20, 10);
INSERT INTO Asignatura VALUES (302, 'Ingles', 25, 8);
INSERT INTO Asignatura VALUES (404, 'Redes', 15, 14);

--Datos de prueba
SELECT * FROM Asignatura;

--Se insertan datos de prueba
INSERT INTO Alumno VALUES (5839201746, 'Juan', 'Perez', 'Lopez', 20);
INSERT INTO Alumno VALUES (1048375926, 'Ana', 'Garcia', 'Torres', 19);
INSERT INTO Alumno VALUES (9274610385, 'Luis', 'Martinez', 'Sanchez', 21);
INSERT INTO Alumno VALUES (3157094826, 'Maria', 'Hernandez', 'Diaz', 22);
INSERT INTO Alumno VALUES (8462019375, 'Carlos', 'Ramirez', 'Morales', 18);
INSERT INTO Alumno VALUES (2905837461, 'Sofia', 'Flores', 'Vargas', 20);
INSERT INTO Alumno VALUES (7649201358, 'Diego', 'Castro', 'Ortega', 23);
INSERT INTO Alumno VALUES (1384759206, 'Elena', 'Ruiz', 'Navarro', 19);
INSERT INTO Alumno VALUES (6592018473, 'Jorge', 'Mendoza', 'Rios', 24);
INSERT INTO Alumno VALUES (4728193056, 'Valeria', 'Cruz', 'Silva', 21);

--Datos de prueba
SELECT * FROM Alumno;

--Se insertan datos de prueba
INSERT INTO Cursa VALUES (5839201746, 103, 9.0);
INSERT INTO Cursa VALUES (1048375926, 105, 8.5);
INSERT INTO Cursa VALUES (9274610385, 201, 7.5);
INSERT INTO Cursa VALUES (3157094826, 204, 9.2);
INSERT INTO Cursa VALUES (8462019375, 302, 8.8);

--Datos de prueba
SELECT * FROM Cursa;

/* Procedimientos almacenados */
GO

/*Traere la logica realizada en las funciones de python a la base de datos
para que los procesos que se repitan solo sean llamados */
---SP para insertar alumno
CREATE PROCEDURE sp_InsertarAlumno
	@noCuenta BIGINT,
	@nombreA VARCHAR(50),
	@apPatA VARCHAR(50),
	@apMatA VARCHAR(50),
	@edadA INT
AS
BEGIN
	SET NOCOUNT ON;
	--Comprobamos que si existe el registro del alumno 
	IF EXISTS (SELECT 1 FROM Alumno WHERE noCuenta = @noCuenta)
	BEGIN 
		RAISERROR('El alumno ya existe', 16, 1);
		RETURN
	END
	--Si no existe el registro, se realiza
	INSERT INTO Alumno (noCuenta, nombreAlum, apPatAlum, apMatAlum, edadAlum)
	VALUES (@noCuenta, @nombreA, @apPatA, @apMatA, @edadA)
END


---SP para consultar alumnos
GO

CREATE PROCEDURE sp_ConsultarAlumnos
AS 
BEGIN 
	SELECT * FROM Alumno 
END


