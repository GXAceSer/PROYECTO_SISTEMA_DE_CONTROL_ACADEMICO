#Como primer paso debemos crear un entorno virtual, esto por medio de nuestra terminal
#por medio del comando: 
#          virtualenv -p python3 env 
# Donde: 
# virtualenv es la herramienta que cre un entorno aislado de python
# -py python3 es python interpreter
# "env" es el nombre del entorno virtual
#-------------------------------------------------------------------------------------

#Ahora debemos de activar nuestro entorno virtual por medio del comando
#     .\env\Scripts\activate
#Donde
# . nos estamos ubicando actualmente en la carpeta \env
# en la carpeta interna donde estan los ejecutables del entorno (\Scripts)
#y estamos activando el scrip que activa el entorno virtual (activate)
#------------------------------------------------------------------------------------

#pyodbc es una libreria de python que nos sirve para podernos conectar 
#con bases de datos, por lo tanto lo instalaremos por medio del comando
#      pip install pyodbc 
#y para corroborar que se instaló correctamente ocupamos el comando
#      pip list
#----------------------------------------------------------------------------------

#Ahora en otra carpeta vamos a crear el documento para poder realizar la conexion 
#(que es este archivo que se encuentra en la carpeta src). 
#----------------PROGRAMACIÓN-----------------------------------------------------
#Importamos la libreria pyodbc
from dotenv import load_dotenv #Para esto debemos instalar pip install python-dotenv en la terminal
import os
import pyodbc

#Cargamos
load_dotenv()
#Variables .env
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


#---------------------------------FUNCIONES-------------------------------------------------------------------------------------------
#***********************************Funcion conexionBase()****************************************************************************
#Por medio de esta funcion vamos a realizar la conexion a la base de datos donde 
#donde se va a trabajar por medio de la variable connection
def conexionBase():
    #Para poder saber si se esta conectando a la base de datos lo relizaremos mediante 
    #una estructura try.
    try:
        #Si el codigo puede conectar a la base de datos va a mostrar conexion exitosa
        #Esto por medio de la variable connection (que es como si tuvieramos un cable conextado a la bd) donde
        connection = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}")
        #Regresamos la variable connection 
        return connection

    except Exception as ex:
        #SI no logra conectarse a la base de datos
        print("Conexion FALLIDA", ex)
        return None #No regresa nada

#******************************************* registrarAlumno()*********************************************************************
def registrarAlumno():
    try: 
        #Si se logra conectar con la base de datos va a retornar la variable de la conexion
        #por lo tanto esa se la asignamos a una variable para poder trabajar con la base de datos
        #y poder crear el cursor
        conexion = conexionBase()
        #Creamos el cursor
        cursor = conexion.cursor()

        #Ahora vamos a pedir al usuario los datos del alumno que se desean agregar a la base de datos
        print("\n --REGISTRAR ALUMNO--")
        #Variables donde se van a guardar los valores
        noCuenta = int(input("No. Cuenta: "))
        cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ? ", (noCuenta,)) #ponemos una coma para que python lo trate como tupla
        #Creamos 
        alumno = cursor.fetchone()

        #Para saber si se encontro el alumno con el numero de cuenta asociado 
        if alumno: #Si  se encuentra el alumno se va a mostrar el siguiente mensaje
            print("ALUMNO YA REGISTRADO")
            return
        else: #Si se encontro al alumno mostramos sus datos:
              
            nombreAlum = input("Nombre(s): ")
            apPatAlum = input("Apellido Paterno: ")
            apMatAlum = input("Apellido Materno: ") 
            edadAlum = int(input("Edad: "))

            #Ahora vamos a realizar la consulta para ingresar los datos obtenidos a la base de datos
            cursor.execute(""" EXEC sp_InsertarAlumno ?, ?, ?, ?, ? """, (noCuenta, nombreAlum, apPatAlum, apMatAlum, edadAlum))

            #Ahora vamos a subirlos a la base de datos
            conexion.commit()

            #Le indicamos al usuario que se registro el alumno
            print("Alumno registrado CORRECTAMENTE")

    except Exception as ex:
        #Si no se logra realizar el registro del alumno va a mostrar el mensaje
        print("ERROR AL REGISTRAR")
        print("ERROR DESDE SQL", ex)
    
    #Como buena practica de programacion abrimos la conexion, usamos y cerramos
    #por ende cerramos por medio:
    finally: 
        if conexion: 
            conexion.close()

#*****************************************************MOSTRAR ALUMNOS******************************************************************************************************************************
def mostrarAlumnos():
    try: #Si logra mostrar los alumnos
        #Variables para el uso de la base de datos y creacion del cursor
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Vamos a realizar la consulta para poderlos mostrar
        cursor.execute("{CALL sp_ConsultarAlumnos}") #Mandamos a llamar nuestro proceso almacenado

        #Ahora los imprimimos por medio de un ciclo for
        for fila in cursor:
            print(f"No.Cuenta: {fila.noCuenta} Nombre(s): {fila.nombreAlum} Apellido Paterno: {fila.apPatAlum} Apellido Materno: {fila.apMatAlum} Edad: {fila.edadAlum}")


    except Exception as ex:
        #Si no se logra mostrar los alumnos se mostrará el siguiente mesnaje
        print("ERROR PARA MOSTRAR DATOS")
        print("ERROR EN SQL", ex)

    finally: 
        if conexion:#   Cerramos la conexion con la base de datos
            conexion.close()

#**************************************EDITAR ALUMNO***********************************************************************************************************************
def editarAlumno():
    try: #Si se logra conectar a la base de datos
        conexion = conexionBase()
        #Creamos el cursor para trabajar con la base
        cursor = conexion.cursor() 

        #Ahora vamos a pedirle al usuario el numero de cuenta del alumno que quiere modificar
        print("Ingrese el NUMERO DE CUENTA del ALUMNO A MODIFICAR")
        noCuentaMod = int(input("No.Cuenta:"))
        #Vamos a realizar la busqueda para mostrarle al usuario si es correcto el alumno que quiere cambiar
        cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ? ", (noCuentaMod,)) #ponemos una coma para que python lo trate como tupla
        #Creamos 
        alumno = cursor.fetchone()

        #Para saber si se encontro el alumno con el numero de cuenta asociado 
        if alumno is None: #Si no se encuentra el alumno se va a mostrar el siguiente mensaje
            print("ALUMNO NO ENCONTRADO")
            return
        else: #Si se encontro al alumno mostramos sus datos:
            print("Datos asociados al Número de cuenta ingresado: ")
            print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum} Edad: {alumno.edadAlum}")
        
        #Si los datos mostrados son los correctos permitimos que pueda editarlos, pero si no, no se le dara permiso
        verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea modificar? (Si/No)").lower()
        if verificacion  == "si" : 
            while True:
                print("DATO A MODIFICAR")
                print("1.NOMBRE")
                print("2.APELLIDO PATERNO")
                print("3.APELLIDO MATERNO")
                print("4.EDAD")
                print("5.SALIR")
                #Opcion 
                opcion = input("Seleccione una opción: ")
                if opcion == "1": #NOMBRE
                    #Le pedimos el nuevo nombre al usuario
                    nuevoNombreAlum = input("Ingrese el NUEVO nombre del número de cuenta ingresado: ")
                    #Realizamos la consulta 
                    cursor.execute("UPDATE Alumno SET nombreAlum = ? WHERE noCuenta = ?", (nuevoNombreAlum, noCuentaMod))
                    #Subimos el cambio a la base de datos
                    conexion.commit()
                    #Mostramos mensaje que se logro el cambio 
                    print("NOMBRE DEL ALUMNO ACTUALIZADO CORRECTAMENTE")

                elif opcion == "2":#APELLIDO PATERNO
                    #Le pedimos el nuevo apellido paterno al usuario
                    nuevoApPatAlum = input("Ingrese el NUEVO apellido Paterno del número de cuenta ingresado: ")
                    #Realizamos consulta
                    cursor.execute("UPDATE Alumno SET apPatAlum = ? WHERE noCuenta = ?", (nuevoApPatAlum, noCuentaMod))
                    #Subimos el cambio a la base de datos
                    conexion.commit()
                    #Mostramos mensaje que se logro el cambio 
                    print("APELLIDO PATERNO DEL ALUMNO ACTUALIZADO CORRECTAMENTE")

                elif opcion == "3": #APELLIDO MATERNO
                    #Le pedimos el nuevo apellido Materno al usuario
                    nuevoApMatAlum = input("Ingrese el NUEVO apellido Materno del número de cuenta ingresado: ")
                    #Realizamos consulta
                    cursor.execute("UPDATE Alumno SET apMatAlum = ? WHERE noCuenta = ?", (nuevoApMatAlum, noCuentaMod))
                    #Subimos el cambio a la base de datos
                    conexion.commit()
                    #Mostramos mensaje que se logro el cambio 
                    print("APELLIDO MATERNO DEL ALUMNO ACTUALIZADO CORRECTAMENTE")

                elif opcion == "4": #EDAD
                    #Le pedimos la nueva edad al usuario
                    nuevaEdadAlum = int(input("Ingrese la NUEVA edad del número de cuenta ingresado: "))
                    if nuevaEdadAlum < 0: #Si la edad es menor a 0 
                        print("EDAD INVÁLIDA") #se muestra que esa edad no es valida
                    else:# en caso de que sea mayor 
                        #Realizamos la consulta
                        cursor.execute("UPDATE Alumno SET edadAlum = ? WHERE noCuenta = ? ", (nuevaEdadAlum, noCuentaMod))
                        #subimos cambios a la base de datos
                        conexion.commit()
                        #Mostramos mensaje que se logro el cambio 
                        print("EDAD DEL ALUMNO ACTUALIZADA CORRECTAMENTE")

                elif opcion == "5": #SALIR
                    print("SALIENDO")
                    break

                else: #SI SE INGRESA UNA OPCION INCORRECTA
                    print("OPCION NO VALIDA")
            
        else:
            print("OPERACIÓN CANCELADA")

    #Si esta ingresando un valor no valido
    except ValueError:
        print("Debes ingresar un número valido")
    #Si no se logra editar alumno
    except Exception as ex:
        print("ERROR EDITAR ALUMNO", ex) #Va a mostrar el mensaje error y de que error se trata
    
    finally: #se cierra la conexion 
        if conexion:  # en caso de que si exista la conexion
            conexion.close()

#**************************************ELIMINAR ALUMNO***********************************************************************************************************************
def eliminarAlumno():
    try: #Si hay conexion 
        #Creación del cursor
        conexion  = conexionBase()
        cursor = conexion.cursor()

        #Le pediremos el numero de cuenta que quiere eliminar el usuario 
        noCuentaElim = int(input("Ingrese el número de cuenta que desea ELIMINAR: "))

        #Ahora realizamos la consulta para encontrar los datos del numero de cuenta que se ingresaron
        cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaElim ,))
        alumno = cursor.fetchone()
        #Condicion para decirle que si existe o no el numero de cuenta que ingreso 
        if alumno is None: 
            print("ALUMNO NO ENCONTRADO")
            return
        else: 
            print("Datos asociados al Número de cuenta ingresado: ")
            print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum} Edad: {alumno.edadAlum}")
        
        print("Si el ALUMNO está INSCRITO en al menos UNA ASIGNATURA, NO SE PUEDE ELIMINAR")
        #Verificamos que el alumno esta o no inscrito en alguna asignatura
        cursor.execute("SELECT * FROM Cursa WHERE noCuenta = ? ", (noCuentaElim,))
        relacion = cursor.fetchone()
        if relacion: #Sí esta inscrito en una materia 
            print("NO SE PUEDE ELIMINAR ALUMNO, YA QUE ESTÁ INSCRITO EN ALGUNA/S ASIGNATURA/S")
        else:
            #Verificamos que los datos mostrados son los correctos, para que este seguro el usuario que es el alumno que desea borrar
            verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea eliminar? (Si/No)").lower()
            if verificacion == "si":
                #Realizamos la consulta
                cursor.execute("DELETE FROM Alumno WHERE noCuenta = ?", (noCuentaElim, ))
                #Subimos el cambio a la base de datos
                conexion.commit()
                #Mostramos el mensaje que se logro la eliminacion del alumno 
                print("ALUMNO ELIMINADO DE LA BASE DE DATOS CORRECTAMENTE")
            else: 
                print("OPERACIÓN CANCELADA")
    except Exception as ex: 
        print("ERROR ELIMINAR ALUMNO", ex)
    finally:
        if conexion: 
            conexion.close()
#**************************************REGISTRAR MATERIA***********************************************************************************************************************
def registrarAsignatura():
    try: #Si hay conexion con la base de datos
        #cursor
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Ahora le vamos a pedir al usuario los datos de la materia que se desea agregar en la bd
        print("\n ------REGISTRAR ASIGNATURA------")
        #Variables para guardar los datos de la nueva asignatura
        idAsig = int(input("Ingrese el ID de la asignatura: "))
        nombreAsign = input("Ingrese el nombre de la asignatura: ")
        cupoAsig = int(input("Ingrese el numero del cupo de la asignatura: "))
        creditosAsig = int(input("Ingrese el numero de creditos de la asignatura: "))

        #Ahora realizamos la consulta 
        cursor.execute("""INSERT INTO Asignatura (idAsign, nombreAsign, cupo, creditos) VALUES (? , ? , ? , ?)""", (idAsig, nombreAsign, cupoAsig, creditosAsig))

        #Lo subimos a la base de datos
        conexion.commit()

        #Le indicamos al usuario que se registro correctamente la asignatura
        print("Asignatura registrada CORRECTAMENTE")
    
    except Exception as ex: #Si no se logra la conexion 
        print("ERROR AL REGISTRAR ASIGNATURA", ex)
    
    #Finalizamos la conexion a la base de datos
    finally:
        if conexion:
            conexion.close()

#**************************************MOSTRAR MATERIA***********************************************************************************************************************
def mostrarAsignatura():
    try: #Si logra tener conexion 
        #Creamos el cursor con la conexion a la base de datos
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Realizamos la consulta para mostrar las asignaturas
        cursor.execute("SELECT * FROM Asignatura")

        #Ahora mostramos los datos obtenidos de la base de datos
        for fila in cursor: 
            print(f"ID Asignatura: {fila.idAsign} Nombre: {fila.nombreAsign} Cupo: {fila.cupo} Creditos: {fila.creditos}")

        #Si no se logra tener conexion 
    except Exception as ex:
        print("ERROR PARA MOSTRAR DATOS", ex)
    
    #Cerramos conexion 
    finally: 
        if conexion:
            conexion.close()

#**************************************ASIGNAR CALIFICACION***********************************************************************************************************************
def asignarCalificacion():
    try: #Si se tiene conexion con la base de datos 
        #Creamos el cursor
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Ahora le vamos a pedir el numero de cuenta del alumno que quiera asignar calificacion 
        noCuentaAlum = int(input("Ingrese el Número de Cuenta del alumno"))

        #Ahora validamos que el alumno exista 
        cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaAlum ,))
        #Ahora vamos a ocupar una variable para saber si existe el alumno o no 
        alumno = cursor.fetchone() 
        if alumno is None : #Si el alumno no exite
            print("ALUMNO NO ENCONTRADO")
            print("--OPERACION CANCELADA--")
            return #nos regresa al menu
        else: #Si el alumno sí existe
            print("---ALUMNO ENCONTRADO---")
            #Mostramos sus datos
            print("Datos asociados al Número de cuenta ingresado: ")
            print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum} Edad: {alumno.edadAlum}")
            
            #Verificamos con el usuario si los datos mostrados son los correctos al numero ingresado
            verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea asignarle calificación? (Si/No)").lower()

            if verificacion == "si": #Si los datos concuerdan 
                #Vamos a mostrar los id con los nombres para que no haya errores de ID de materias
                cursor.execute("SELECT idAsign, nombreAsign FROM Asignatura")
                for fila in cursor:  #Mostramos la informacion de la consulta
                    print(f"ID Asignatura: {fila.idAsign} Nombre: {fila.nombreAsign}")

                #vamos a pedirle los datos faltantes para cumplir la asignacion de calificacion
                idAsigCali = int(input("Ingrese el ID de la Asignatura: "))

                #Debemos comporbar que la asignatura existe
                #Realizamos la consulta
                cursor.execute("SELECT * FROM Asignatura WHERE idAsign = ?", (idAsigCali, ))
                asignatura = cursor.fetchone()
                #Validamos 
                if asignatura is None : #Si la asignatura no existe
                    #Mostramos un mensaje diciendo que no existe la asignatura
                    print("ASIGNATURA NO REGISTRADA")
                    print("---OPERACION CANCELADA---")
                    #retornamos al menu principal
                    return
                else: #Si existe la asignatura
                    print("ASIGNATURA REGISTRADA") 

                #Para evitar duplicados por si ya se tiene una calificacion igual
                #Antes de pedirle la calficacion vamos a verificar si el alumno ya tiene calificacion 
                cursor.execute("""SELECT * FROM Cursa WHERE noCuenta = ? AND idAsign = ? """, (noCuentaAlum, idAsigCali))

                #Para no hacer una variable extra podemos hacer la validacion directa
                if cursor.fetchone(): #Si ya existe un registro con los datos ingresados 
                    #Mostramos un mensaje que ya existe una calificacion y que mejor en el menu seleccione la opcion de cambiar calificacion 
                    print("---YA EXISTE UNA CALIFICACIÓN PARA ESTA ASIGNATURA---")
                    print("La puede cambiar seleccionando la opcion para MODIFICAR CALIFICACIÓN")
                    #Lo regresamos al menu principal
                    return

                #pedimos la calificacion
                calificacionAlum = int(input("Ingrese la calificación: "))
                #Validamos que la calificacion ingresada cumpla con los parametros de ser menor que cero o mayor que 10
                if calificacionAlum < 0 or calificacionAlum > 10: 
                    print("CALIFICACION NO VALIDA (ES MENOR A 0 O MAYOR A 10)")
                    return #regresamos
                
                #Ahora vamos a realizar la consulta para ingresar los datos 
                cursor.execute("""INSERT INTO Cursa (noCuenta , idAsign , calificacion ) VALUES (? , ? , ? )""", (noCuentaAlum, idAsigCali, calificacionAlum))

                #Subimos los cambios en la base de datos 
                conexion.commit()

                #Le indicamos al usuario que se registro la calificacion correctamente
                print("----CALIFICACIÓN REGISTRADA CORRECTAMENTE------")

    #Si ingresan valores incorrectos
    except ValueError:
        print("Debes ingresar valores NUMÉRICOS VALIDOS")

    except Exception as ex: #Si no se logra la conexion
        print("ERROR AL ASIGNAR ASIGNATURA", ex)
    
    #Finalizamos la conexion 
    finally:
        if conexion:
            conexion.close()        

#**************************************CONSULTAR CALIFICACION***********************************************************************************************************************
def mostrarCalificaciones(): 
    try: #Si hay conexion con la base de datos
        #Definimos nuestro cursor 
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Se realizaran dos tipos de busqueda 
        print("------------CONSULTAR CALIFICACIONES-----------------")
        print("1. Ver todas las calificaciones del alumno.")
        print("2. Ver calificación de una asignatura que este incrito el alumno.")
        print("0. Salir.")
        opcMenu = input("Ingrese la opción que dese observar: ")

        #Menu 
        if opcMenu == "1": #Ver todas las calificaciones 
            #Vamos a pedirle el noCuenta del alumno 
            noCuentaAlumBusc = int(input("Ingrese el Número de Cuenta del Alumno: "))
            #Validamos que sí exista el alumno 
            cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaAlumBusc ,))
            alumno = cursor.fetchone()
            if alumno is None: #Si no se encuentra al alumno 
                print("--ALUMNO NO REGISTRADO--") 
                return# regresamos al menu 
            
            #Ahora vamos a realizar la consulta para traer todas sus calificaciones 
            cursor.execute("""
            SELECT A.nombreAlum, ASIG.nombreAsign, C.calificacion 
            FROM Cursa C 
            JOIN Alumno A ON C.noCuenta = A.noCuenta 
            JOIN Asignatura ASIG ON C.idAsign = ASIG.idAsign 
            WHERE C.noCuenta = ?
            """, (noCuentaAlumBusc,))
            #Vamos a validar si el alumno tiene calificaciones registradas
            resultados = cursor.fetchall()
            if not resultados: #si no tiene calificaciones registradas
                #se mostrara el mensaje: 
                print("EL ALUMNO NO TIENE CALIFICACIONES REGISTRADAS")
                print("OPERACION CANCELADA")
                return# regresamos al menu
            #Ahora imprimimos las calificaciones 
            print(f"\nCALIFICACIONES DEL ALUMNO {alumno.noCuenta} \n")
            for fila in resultados:
                print(f"Asignatura: {fila[1]} | Calificación: {fila[2]}") 
            
        
        elif opcMenu == "2": #Ver calificacion de una asignatura en especifico
            #Vamos a pedirle el noCuenta del alumno 
            noCuentaAlumBusc = int(input("Ingrese el Número de Cuenta del Alumno: "))
            #Validamos que sí exista el alumno 
            cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaAlumBusc ,))
            alumno = cursor.fetchone()
            if alumno is None: #Si no se encuentra al alumno 
                print("--ALUMNO NO REGISTRADO--") 
                return# regresamos al menu 
        
            #Vamos a pedirle el id de la materia 
            idAsignCal = int(input("Ingrese el ID de la Asignatura: "))
            #Validamos que la asignatura exista 
            cursor.execute("SELECT * FROM Asignatura WHERE idAsign = ? ", (idAsignCal, ))
            asigVerif = cursor.fetchone()
            if asigVerif is None: # Si no existe la asignatura
                print("-----ASIGNATURA NO REGISTRADA-----")
                return #Regresamos al menu
            
            #realizamos consulta 
            cursor.execute("""SELECT C.calificacion, ASIG.nombreAsign
            FROM Cursa C
            JOIN Asignatura ASIG ON C.idAsign = ASIG.idAsign
            WHERE C.noCuenta = ? AND C.idAsign = ?
            """, (noCuentaAlumBusc, idAsignCal))
            datoCalificacion = cursor.fetchone()
            #Validamos que el alumno tenga dicha asignatura
            if datoCalificacion is None: 
                print("EL ALUMNO NO ESTA INSCRITO EN ESA ASIGNATURA")
                return#retornamos 

            #mostramos la informacion 
            print(f"\nNo.Cuenta: {alumno.noCuenta}")
            print(f"\nAlumno: {alumno.nombreAlum} {alumno.apPatAlum} {alumno.apMatAlum}")
            print(f"\nAsignatura: {datoCalificacion.nombreAsign}")
            print(f"\nAlumno: {datoCalificacion.calificacion}")
            
        elif opcMenu == "0": #Salir 
            print("Saliendo de Mostrar Calificaciones")
            return
        
        else: #En caso de que se coloque una opcion que no 
            print("OPCION NO VALIDA")
            return #Lo regresa al menu
        
   
    except Exception as ex: #Si no hay conexion con la bd
        print("--ERROR AL MOSTRAR CALIFICACIONES--", ex)

    finally: #Finalizamos la conexion 
        if conexion: # si hay conexion 
            conexion.close()

#**************************************MODIFICAR CALIFICACION***********************************************************************************************************************
def modificarCalificacion():
    try: #Si hay comunicacion con la base de datos
        #Creamos el cursor
        conexion = conexionBase()
        cursor = conexion.cursor()

        print(f"\n--------MODIFICAR CALIFICACIÓN---------\n")

        #Ahora le vamos a preguntar al usuario el numero de cuenta del alumno que desea modificar su calificacion 
        alumCali = int(input("Ingrese el numero de cuenta del alumno: "))
        #Ahora verficaremos que el alumno este registrado en la base de datos por medio de una consulta
        cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (alumCali ,))
        alumno = cursor.fetchone()
        if alumno is None: #Si no se encuentra al alumno 
            print("--ALUMNO NO REGISTRADO--") 
            return# regresamos al menu 
        else: #Si se encuentra registrado el alumno vamos a mostrarle los datos del alumno para que corrobore el usuario 
            print("---ALUMNO ENCONTRADO---")
            #Mostramos sus datos
            print("Datos asociados al Número de cuenta ingresado: ")
            print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum} Edad: {alumno.edadAlum}")
            
        
        #Verificamos con el usuario si los datos mostrados son los correctos al numero ingresado
        verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea modificar la calificación? (Si/No)").lower()

        if verificacion == "si":        
            #ahora vamos a solicitarle la asignatura al usuario, para evitar
            #errores hay que mostrarles las asignaturas con su respectivo ID
            #Vamos a mostrar los id con los nombres para que no haya errores de ID de materias
            cursor.execute("SELECT idAsign, nombreAsign FROM Asignatura")
            for fila in cursor:  #Mostramos la informacion de la consulta
                print(f"ID Asignatura: {fila[0]} Nombre: {fila[1]}")
            asignaturaCali = int(input("Ingrese el ID de la asignatura: "))

            #Ahora vamos a corroborar que exista la asignatura
            cursor.execute("SELECT * FROM Asignatura WHERE idAsign = ? ", (asignaturaCali, ))
            asigVerif = cursor.fetchone()
            if asigVerif is None: # Si no existe la asignatura
                print("-----ASIGNATURA NO REGISTRADA-----")
                return #Regresamos al menu
            
                #Ahora vamos a corroborar que el alumno este inscrito en esa materia 
            else: 
                cursor.execute("""SELECT C.calificacion, ASIG.nombreAsign
                FROM Cursa C
                JOIN Asignatura ASIG ON C.idAsign = ASIG.idAsign
                WHERE C.noCuenta = ? AND C.idAsign = ?
                """, (alumCali, asignaturaCali))
                datoCalificacion = cursor.fetchone()
                #Validamos que el alumno tenga dicha asignatura
                if datoCalificacion is None: 
                    print("EL ALUMNO NO ESTA INSCRITO EN ESA ASIGNATURA")
                    return#retornamos 
                
                else: #que el usuario ingrese la nueva calificacion 
                    #Mostramos la calificacion asignada previamente 
                    print(f"Calificación actual: {datoCalificacion[0]}")
                    nuevaCalificacion = int(input("Ingrese la nueva calificacion: "))
                    #Corroboramos que la calificacion ingresada cumpla con los parametros de ser menor que cero o mayor a 10
                    if nuevaCalificacion < 0 or nuevaCalificacion > 10:
                        print("CALIFICACION NO VALIDA (ES MENOR A 0 O MAYOR A 10)")
                        return #regresamos al menu
                    else:
                        #Realizamos la consulta para ingresar los datos
                        cursor.execute("""UPDATE Cursa SET calificacion = ? WHERE noCuenta = ? AND idAsign = ? """, (nuevaCalificacion, alumCali, asignaturaCali))
                        #Subimos los cambios en la base de datos
                        conexion.commit()
                        #Indicamos que la calificacion ha sido modificada
                        print("-----CALIFICACION MODIFICADA CORRECTAMENTE-----")

    except Exception as ex: #Si no hay conexion a la bd
        print("ERROR PARA MOSTRAR CALIFICACIONES", ex)
    
    finally: #Finalizamos la conexion 
        if conexion: #si hay conexion 
            conexion.close() #se cierra            


#**************************************PROMEDIOS Y REPORTES***********************************************************************************************************************
def PromediosYReportes(): 
    try: #Si se tiene conexion con la base de datos
        #Creamos cursor para tener conexion con la base
        conexion = conexionBase()
        cursor = conexion.cursor()

        #Vamos a hacer un menu donde va a mostrar las opciones de promedio por alumno, promedio por materia y 
        #estado(Arpobado/ reprobado)
        print("------PROMEDIOS Y REPORTES-----")
        print("1. Promedio por alumno")
        print("2. Promedio por asignatura")
        print("3. Estado (Aprobado/Reprobado por alumno)")
        print("0. Salir")

        opcionMen = input("Ingrese la opcion que desee realizar: ")

        if opcionMen == "1": #Promedio alumno 
            print("---PROMEDIO ALUMNO---")
            #Primero vamos a pedirle el numero de cuenta del alumno 
            noCuentaAlumProm = int(input("Ingrese el número de cuenta del Alumno: "))

            #Vamos a corroborar que el alumno exista
            cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaAlumProm ,))
            alumno = cursor.fetchone()
            if alumno is None: #Si no se encuentra al alumno 
                print("--ALUMNO NO REGISTRADO--") 
                return# regresamos al menu 
            else: #Si se encuentra registrado el alumno vamos a mostrarle los datos del alumno para que corrobore el usuario 
                print("---ALUMNO ENCONTRADO---")
                #Mostramos sus datos
                print("Datos asociados al Número de cuenta ingresado: ")
                print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum}")
            
            #Verificamos con el usuario si los datos mostrados son los correctos al numero ingresado
            verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea consultar el promedio? (Si/No)").lower()
            if verificacion == "si": 
                #Vamos a corroborar si el alumno esta inscrito en las asignaturas
                #Si no esta inscrito en las asignaturas 
                cursor.execute("SELECT COUNT(*) FROM Cursa WHERE noCuenta = ?", (noCuentaAlumProm ,))
                cantidadAlum = cursor.fetchone()[0]
                if cantidadAlum == 0: #Si no esta inscrito y no tiene calificaciones:
                    print(f"El alumno no está inscrito en ninguna asignatura")
                else: #Si esta inscrito
                    #Realizamos la consulta para obtener el promedio 
                    cursor.execute("SELECT AVG(calificacion) FROM Cursa WHERE noCuenta = ?", (noCuentaAlumProm , ))
                    promedio = cursor.fetchone()[0]
                    #mostramos el promedio 
                    print(f"No.Cuenta Alumno: {alumno.noCuenta}")
                    print(f"Promedio: {round(promedio,2)}")
            else: 
                print("OPERACION CANCELADA") #
                return

        elif opcionMen == "2": #Promedio por Asignatura
            print("---- PROMEDIO POR ASIGNATURA ---")
            #Mostramos las asignaturas con sus respectivos ID
            cursor.execute("SELECT * FROM Asignatura")

            #Ahora mostramos los datos obtenidos de la base de datos
            for fila in cursor: 
                print(f"ID Asignatura: {fila.idAsign} Nombre: {fila.nombreAsign} Cupo: {fila.cupo} Creditos: {fila.creditos}")

            #Le solicitamos el ID de la asignatura
            idAsignProm = int(input("Ingrese el ID de la asignatura: ")) 
            #Verificamos que exista la asignatura 
            cursor.execute("SELECT * FROM Asignatura WHERE idAsign = ?", (idAsignProm, ))
            asignatura = cursor.fetchone()
            if asignatura is None: #Si no hay una asignatura con ese ID
                print("ASIGNATURA NO REGISTRADA") #Se va a mostrar este mensaje 
            else: 
                #Verificamos que tenga alumnos inscritos 
                cursor.execute("SELECT COUNT(*) FROM Cursa WHERE idAsign = ?", (idAsignProm,))
                cantidad = cursor.fetchone()[0]
                if cantidad == 0:   #Si no tiene alumnos inscritos le mostramos el siguiente mensaje 
                    print("ESTA ASIGNATURA NO TIENE ALUMNOS INSCRITOS")
                else: #Si tiene alumnos inscritos 
                    #Obtenemos el promedio 
                    cursor.execute("SELECT AVG(calificacion) FROM Cursa WHERE idAsign = ?" , (idAsignProm, ))
                    promedioAsign = cursor.fetchone()[0]
                    #Mostramos el promedio 
                    print(f"ID Asignatura: {asignatura.idAsign}")
                    print(f"Nombre Asignatura: {asignatura.nombreAsign}")
                    print(f"Promedio = {round(promedioAsign,2)}")
            
        elif opcionMen == "3":#Estado por alumno
            #Pedimos el numero de cuenta del alumno que quieren consultar 
            noCuentaAlumEstado = int(input("Ingrese el número de cuenta del Alumno: "))

            #Vamos a corroborar que el alumno exista
            cursor.execute("SELECT * FROM Alumno WHERE noCuenta = ?", (noCuentaAlumEstado ,))
            alumno = cursor.fetchone()
            if alumno is None: #Si no se encuentra al alumno 
                print("--ALUMNO NO REGISTRADO--") 
                return# regresamos al menu 
            else: #Si se encuentra registrado el alumno vamos a mostrarle los datos del alumno para que corrobore el usuario 
                print("---ALUMNO ENCONTRADO---")
                #Mostramos sus datos
                print("Datos asociados al Número de cuenta ingresado: ")
                print(f"No.Cuenta: {alumno.noCuenta} Nombre(s): {alumno.nombreAlum} Apellido Paterno: {alumno.apPatAlum} Apellido Materno: {alumno.apMatAlum}")
            
            #Verificamos con el usuario si los datos mostrados son los correctos al numero ingresado
            verificacion = input("¿Los datos mostrados concuerdan con el del alumno que desea saber el estado? (Si/No)").lower()
            if verificacion == "si":
                #Realizamos la consulta para saber el promedio del alumno
                cursor.execute("SELECT AVG(calificacion) FROM Cursa WHERE noCuenta = ?", (noCuentaAlumEstado , ))
                promedio = cursor.fetchone()[0]
                #Corroboramos que el alumno tenga calificaciones
                if promedio is None: 
                    print("El alumno NO TIENE CALIFICACIONES REGISTRADAS")
                else: 
                    #Realizamos la comparación
                    if promedio >= 6 : #Si su promedio es mayor a 6
                        print("-------ALUMNO APROBADO---------")
                        print(f"No.Cuenta Alumno: {alumno.noCuenta}")
                        print(f"Alumno: {alumno.nombreAlum} {alumno.apPatAlum} {alumno.apMatAlum}")
                        print(f"Promedio: {round(promedio,2)}")
                    else: #Si su promedio es menor que 6
                        print("-------ALUMNO REPROBADO---------")
                        print(f"No.Cuenta Alumno: {alumno.noCuenta}")
                        print(f"Alumno: {alumno.nombreAlum} {alumno.apPatAlum} {alumno.apMatAlum}")
                        print(f"Promedio: {round(promedio,2)}")
                        
            else: #Si los datos no concuerdan
                print("OPERACION CANCELADA")
                return #lo regresa al menu principal
            
        elif opcionMen == "0": #Salir
            print("SALIENDO")
            return
        else: #Si se ingresa una opcion no valida
            print("OPCIÓN NO VALIDA")
            return

    except Exception as ex: #Si no hay conexion con la bd
        print("ERROR PARA MOSTRAR PROMEDIO", ex)
    finally: #Cerramos conexion 
        if conexion: #Si hay conexion 
            conexion.close() #Cerramos


#----------------------------------MENU------------------------------------------------------------------------------------------------------------------------------------
#Creamos un menu para poder interactuar con el usuario para que pueda ocupar correctamente la base de datos
while True: #Mientras se eliga una opcion valida se va a mostrar el menu 
    print("\n ....:::: M E N Ú ::::....")
    print("1. Registrar alumno.")
    print("2. Mostrar alumnos")
    print("3. Editar alumno")
    print("4. Eliminar alumno")
    print("5. Registrar asignatura")
    print("6. Mostrar asignaturas")
    print("7. Asignar calificación")
    print("8. Consultar calificación")
    print("9. Modificar calificación")
    print("10. Promedios y Reportes")
    print("0. Salir")

    #La variable opcion va a guardar la opcion que eliga el usuario
    opcion = input("Ingrese el número de la opción que dese realizar: ")

    #Ocupamos las estructuras if y elif para mandar llamar las funciones de lo que desee realizar 
    if opcion == "1": #Si se ingresa el numero 1 
        registrarAlumno() #Se va a realizar lo de la funcion registrarAlumno()
    elif opcion == "2": #Si se ingresa el numero 2
        mostrarAlumnos() #Se va a realizar lo de la funcion mostrarAlumnos()
    elif opcion == "3": 
        editarAlumno() #Editar alumno 
    elif opcion == "4": 
        eliminarAlumno() #Editar alumno 
    elif opcion == "5": 
        registrarAsignatura() #Registrar Asignatura
    elif opcion == "6": 
        mostrarAsignatura() #Mostrar Asignatura
    elif opcion == "7": 
        asignarCalificacion() #Asignar calificacion 
    elif opcion == "8": 
        mostrarCalificaciones() #Mostrar Calificaciones
    elif opcion == "9":
        modificarCalificacion() #Modificar Calificacion 
    elif opcion == "10":
        PromediosYReportes() #Promedios y reportes
    elif opcion == "0": #Si se ingresa el numero 0
        print("Saliendo ¡Hasta Luego!") #Se sale y se cierra la conexion con la base de datos.
        break
    else: #En caso de ingresar un dato que no sea correcto
     print("Opción no válida") #Se muestra este mensaje

    




    





