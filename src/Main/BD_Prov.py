import os
import sqlite3
from Main import Rest_Main
try:
    BD='Provincias'
    Cone=sqlite3.connect(BD)
    Curs= Cone.cursor()
    print("Base de datos de provincias conectada") 
except sqlite3.OperationalError as e:
    print(e)
    
def Load(ListPro):
    #Carga de datos
    try:
        ListPro.clear()
        Curs.execute("SELECT provincia FROM Provincias")
        for row in Curs:
            ListPro.append(row)
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
    
def LoadCiu(ListCiu,Provincia):
    #Carga de datos
    try:
        ListCiu.clear()
        Provincia = Provincia + 1
        Curs.execute("SELECT municipio FROM Municipios WHERE provincia_id = "+str(Provincia))
        for row in Curs:
            ListCiu.append(row)
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()
        
def IDProv(ID):
    #Carga de datos
    try:
        ID = ID + 1
        Curs.execute("SELECT provincia FROM Provincias WHERE id = "+str(ID))
        for row in Curs:
            return row
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()

def IDCiu(ID):
    #Carga de datos
    try:
        ID = ID + 1
        Curs.execute("SELECT municipio FROM Municipios WHERE id = "+str(ID))
        for row in Curs:
            return row
    except sqlite3.OperationalError as e:
        print(e)
        Cone.rollback()