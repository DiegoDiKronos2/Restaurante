
import os
import sqlite3
from Main import Rest_Main
from asn1crypto._ffi import null
try:
    BD='RestBD.db'
    Cone=sqlite3.connect(BD)
    Curs= Cone.cursor()
    print("Base de datos conectada") 
except sqlite3.OperationalError as e:
    print(e)

############################# Métodos de carga de datos ############################
def LogCompr(Log):
    try:
        Curs.execute("SELECT * FROM Camarero WHERE (Nombre = ?) AND (Contraseña = ?)",(Log[0],Log[1]))
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs

def Load(ID):
    try:
        if ID == 0:
            Curs.execute("SELECT * FROM Mesa")
        elif ID == 1:
            Curs.execute("SELECT * FROM Cliente")
        elif ID == 2:
            Curs.execute("SELECT * FROM Servicio")
        elif ID == 3:
            Curs.execute("SELECT * FROM Factura")
        elif ID == 4:
            Curs.execute("SELECT F.IDFact,F.DNICliente,C.Nombre,F.IDMesa,F.Fecha FROM Factura AS F INNER JOIN Camarero AS C ON F.IDCam = C.IDCam")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadFactFilter(IDMesa):
    try:
        Curs.execute("SELECT F.IDFact,F.DNICliente,C.Nombre,F.IDMesa,F.Fecha FROM Factura AS F INNER JOIN Camarero AS C ON F.IDCam = C.IDCam WHERE IDMesa = '"+str(IDMesa)+"'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadFactFilterDNI(DNI):
    try:
        Curs.execute("SELECT F.IDFact,F.DNICliente,C.Nombre,F.IDMesa,F.Fecha FROM Factura AS F INNER JOIN Camarero AS C ON F.IDCam = C.IDCam WHERE DNICliente = '"+str(DNI)+"'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadFactLite(IDMesa):
    try:
        Curs.execute("SELECT * FROM Factura WHERE IDMesa = '"+str(IDMesa)+"'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadLF(IDF):
    try:
        Curs.execute("SELECT S.Servicio, S.PrecioUnidad, LF.Cantidad FROM LineaFactura AS LF INNER JOIN Servicio AS S ON LF.IDServicio = S.IDServicio WHERE LF.IDFactura = '"+str(IDF)+"'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadOnService(IDF):
    try:
        Curs.execute("SELECT F.IDMesa, Ca.Nombre, Cl.Nombre FROM Factura AS F INNER JOIN Cliente AS Cl ON F.DNICliente = Cl.DNI INNER JOIN Camarero AS Ca ON F.IDCam = Ca.IDCam WHERE IDFact =  '"+str(IDF)+"'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def LoadOccuped():
    try:
        Curs.execute("SELECT * FROM Mesa WHERE (Ocupada = 'Si')")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs

def SearchCli(TEXT):
    try:
        Curs.execute("SELECT * FROM Cliente WHERE Apellidos like '"+TEXT+"%'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs
def SearchService(TEXT):
    try:
        Curs.execute("SELECT * FROM Servicio WHERE Servicio like '"+TEXT+"%'")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs

def FindClient(DNI):
    try:
        Curs.execute("SELECT * FROM Cliente WHERE (DNI = '"+DNI+"')")
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs.fetchall()

def LoadToFactura(IDF):
    try:
        Curs.execute('SELECT F.IDVenta, S.Servicio, F.Cantidad, S.PrecioUnidad FROM LineaFactura AS F INNER JOIN Servicio AS S ON S.IDServicio = F.IDServicio WHERE IDVenta = ', (IDF,))
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs.fetchall()
def LoadToCabecera(idfactura):
    try:
        Curs.execute("SELECT Nombre from Camarero AS C INNER JOIN Factura AS F where F.IDFact = ? and C.IDCam = F.IDCam",(idfactura,))
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs.fetchall()
############################# Métodos de inserción de datos ############################
def Insert(fila, ID):
    try:
        if ID == 0:
            Curs.execute("INSERT INTO Cliente (DNI,Apellidos,Nombre,Direccion,Provincia,Ciudad)"
                         +" VALUES (?,?,?,?,?,?)",fila)
            Cone.commit()
        elif ID == 1:
            Curs.execute("INSERT INTO Servicio (Servicio,PrecioUnidad) VALUES (?,?)",(fila[0],fila[1]))
            Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
        
def InsertSF(IDF,IDS):
    try:
        IDF = str(IDF)
        IDS = str(IDS)
        Curs.execute("SELECT * FROM LineaFactura WHERE IDFactura = "+IDF+" AND IDServicio = "+IDS)
        data = 0
        for i in Curs:
            data = i[3]
        if data >= 1:
            Curs.execute("UPDATE LineaFactura SET Cantidad = "+str(data+1)+" WHERE IDFactura = "+IDF+" AND IDServicio = "+IDS)
            Cone.commit()
        else:
            fila = (IDF,IDS,"1")
            Curs.execute("INSERT INTO LineaFactura (IDFactura,IDServicio,Cantidad) VALUES (?,?,?)",fila)
            Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()

############################# Métodos de modificación de datos ############################
def Ocupped(fila):
    try:
        Curs.execute("UPDATE Mesa SET Ocupada='Si' WHERE IDMesa = ?",(fila[0],))
        Cone.commit()
        Curs.execute("INSERT INTO Factura (DNICliente,IDCam,IDMesa,Fecha) VALUES (?,?,?,?)",(fila[1],fila[2],fila[0],fila[3]))
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
    
############################# Métodos de borrado de datos ############################

def DelClient(DNI):
    try:
        Curs.execute("DELETE FROM Cliente WHERE (DNI = '"+DNI+"')")
        Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    return Curs.fetchall()

def DelLF(IDF,IDS):
    try:
        IDF = str(IDF)
        IDS = str(IDS)
        Curs.execute("SELECT LF.IDVenta,LF.Cantidad FROM LineaFactura AS LF "+
                     "INNER JOIN Servicio AS S ON S.IDServicio = LF.IDServicio "+
                     "INNER JOIN Factura AS F ON LF.IDFactura = F.IDFact "+
                     "WHERE S.Servicio = '"+IDS+"' AND F.IDFact = "+IDF)
        data = 0
        for i in Curs:
            data = i[0],i[1]
        if data[1] >= 2:
            Curs.execute("UPDATE LineaFactura SET Cantidad = "+str(data[1]-1)+" WHERE IDVenta = "+str(data[0]))
            Cone.commit()
        else:
            Curs.execute("DELETE FROM LineaFactura WHERE IDVenta = "+str(data[0]))
            Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
def EraseService(ID):
    try:
        Curs.execute("DELETE FROM Servicios WHERE IDServicio = ",ID)
        Cone.commit()
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
def DROPALL():##Elimina todo el contenido de la BBDD
    try:
            Curs.execute("DELETE FROM Clientes")
            Cone.commit()
    except sqlite3.OperationalError as e:
            print(e)
            Cone.rollback()

############################# Métodos de adicionales ############################

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
    