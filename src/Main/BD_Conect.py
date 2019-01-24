
import os
import sqlite3
from Main import Rest_Main
try:
    BD='RestBD.db'
    Cone=sqlite3.connect(BD)
    Curs= Cone.cursor()
    print("Base de datos conectada") 
except sqlite3.OperationalError as e:
    print(e)

############################# Métodos de carga de datos ############################
def LogCompr(Log):
    Curs.execute("SELECT * FROM Camarero WHERE (Nombre = ?) AND (Contraseña = ?)",(Log[0],Log[1]))
    return Curs
def Load(ID):
    #Carga de datos
    if ID == 0:
        Curs.execute("SELECT * FROM Mesa")
    elif ID == 1:
        Curs.execute("SELECT * FROM Reparaciones")
    elif ID == 2:
        Curs.execute("SELECT * FROM Facturaciones")
    
    return Curs
def LoadOccuped():
    try:
        Curs.execute("SELECT * FROM Mesa WHERE (Ocupada = 'Si')")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
############################# Métodos de inserción de datos ############################
def Insert(fila, ID):
    
    if ID == 0:
        try:
            Curs.execute("INSERT INTO Clientes (DNI,Nombre,Apellidos,Matricula,Telefono,EMail,Fecha)"
                         +" VALUES (?,?,?,?,?,?,?)",fila)
            Cone.commit()
    
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 1:
        try:
            Curs.execute("INSERT INTO Reparaciones (ManObra,Matricula,Aceite,Neumaticos,Ruedas,Bateria,Filtros)"
                         +" VALUES (?,?,?,?,?,?,?)",fila)
            Cone.commit()
    
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 2:
        try:
            Curs.execute("INSERT INTO Facturaciones (Fecha,Matricula)"
                         +" VALUES (?,?)",fila)
            Cone.commit()
    
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()

############################# Métodos de modificación de datos ############################
def Ocupped(ID):
    try:
        Curs.execute("UPDATE Mesa SET Ocupada='Si' WHERE IDMesa = ?",(ID,))
        Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
def Disocupped(ID):
    try:
        Curs.execute("UPDATE Mesa SET Ocupada='No' WHERE IDMesa = ?",(ID,))
        Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
def Modificar(fila,ID):
    if ID == 0:
        try:
            Curs.execute("UPDATE CLIENTES "
                    "SET Nombre=?,Apellidos=?,Matricula=?,Telefono=?,EMail=?,Fecha=?"
                    "WHERE DNI=?", (fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[0]))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 1:
        try:
            Curs.execute("UPDATE REPARACIONES "
                         "SET ManObra=?,Matricula=?,Aceite=?,Neumaticos=?,Ruedas=?,Bateria=?,Filtros=?"
                         "WHERE NFacturacion=?", (fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[7],fila[0]))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 2:
        try:
            Curs.execute("UPDATE FACTURACIONES "
                         "SET Matricula=?,Fecha=? "
                         "WHERE IDFact=?", (fila[1],fila[2],fila[0]))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    
############################# Métodos de borrado de datos ############################

def Del(Reference,ID):##Eliminar bajo referencia
    
    if ID == 0:
        try:##Borrar un cliente borra todas las facturas y reparaciones relacionadas
            Curs.execute("SELECT Matricula AS M FROM Clientes WHERE (DNI = ?)",(Reference,))
            Mat = ""
            for i in Curs:
                Mat = i[0]
            Cone.commit()
            
            Curs.execute("DELETE FROM Reparaciones WHERE (Matricula = ?)",(Mat,))
            Cone.commit()
            
            Curs.execute("DELETE FROM Facturaciones WHERE (Matricula = ?)",(Mat,))
            Cone.commit()
            
            Curs.execute("DELETE FROM Clientes WHERE (DNI = ?)",(Reference,))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 1:
        try:
            Curs.execute("DELETE FROM Reparaciones WHERE (NFacturacion = ?)",(Reference,))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
    elif ID == 2:
        try:
            Curs.execute("DELETE FROM Facturaciones WHERE (IDFact = ?)",(Reference,))
            Cone.commit()
        except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()
            
def DROPALL():##Elimina todo el contenido de la BBDD
    try:
            Curs.execute("DELETE FROM Clientes")
            Cone.commit()
            Curs.execute("DELETE FROM Reparaciones")
            Cone.commit()
            Curs.execute("DELETE FROM Facturaciones")
            Cone.commit()
    except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()

############################# Métodos de adicionales ############################

def validoMatricula(Mat): ##Comprueba que ya existe el cliente en la BBDD 
    Curs.execute("SELECT DNI FROM Clientes WHERE (Matricula = ?)",(Mat,))
    Cone.commit()
    Comp = ""
    for i in Curs:
        Comp = i[0]
    if Comp != "":
        return True
    else:
        return False

def AltaLista(Tree,Lista,fila): ##Actualiza la lista mostrada en la interfaz
    Lista.append(fila)
    Tree.show()
    
def Disconect():
    try:
        Cone.commit()
        Cone.close()
        print("Base desconectada")
    except sqlite3.OperationalError as e:
        print(e)
    