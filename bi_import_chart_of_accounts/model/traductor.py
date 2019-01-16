#%%
import csv
import re
import pandas as pd
import numpy as np
import matplotlib as plt



# Variables locales

# columnas: Lista con atributos(columnas) a extraer desde el input.
#           ['RUT',
#            'NOMBRE', 
#            'CLIENTE', 
#            'CENTRO COSTO', 
#            'RAZON SOCIAL', 
#            'CARGO',
#            'REQUIERE FIRMA ELECTRONICA']

# trabajadores:Lista de listas. Cada lista representa a un trabajador del input sometida a un procesamiento
#              El proceso realiza: 
#              - Selección de atributos deseados 
#              - Traducción centro costo a razón social
#              - Especificación de capacitaciones con estado pendiente o cerrado correspondiente a trabajador
#
#  trabajador: Lista. Corresponde a una fila particular del Excel, es una variable auxiliar
#              para la construccion de "trabajadores"            
# 
# capacitacion: Diccionario con todas las capacitaciones. 
# diccionario: Diccionario para traducción de centro de costo a razón social

# total: Lista de objetos Arbeiter. Cada objeto Arbeiter corresponde a una instancia de un trabajador
#        asociada a una unica capacitacion. 
#        Existen n objetos arbeiter por cada n capacitaciones en estado pendiente o cerrado que tenga el trabajador


columnas=[]
trabajadores=[]

capacitacion={}
diccionario={
    "2":"RIVAS Y ASOCIADOS LTDA",
    "3":"EXPROCAP S.A.",
    "5":"EXPROCHILE S.A.",
    "700":"EST EXPROSERVICIOS S.A.",
    "800":"EST EXPROTIEMPO S.A.",
    "900":"EXPROSERVICIOS S.A."}
total=[]
lista_reducida=[]

class SmallWorker():
    def __init__(self,rut,cliente,cargo,cerrado,pendiente):
        
        self.id=rut+"_"+cliente
        self.cargo=cargo
        self.cerrado=cerrado
        self.pendiente=pendiente
        self.total=cerrado+pendiente
        self.p_pend=(pendiente/self.total)*100
        self.p_cerr=(cerrado/self.total)*100


class Arbeiter():
    def __init__(self,rut,nombre,cliente,centrocosto,razonsocial,cargo,requierefirma,capacitacion,estado):
        self.rut=rut
        self.nombre=nombre
        self.cliente=cliente
        self.centrocosto=centrocosto
        self.razonsocial=razonsocial
        self.cargo=cargo
        self.requierefirma=requierefirma
        self.capacitacion=capacitacion
        self.estado=estado
    
    def show(self):
        print(self.rut)
        print(self.nombre)
        print(self.cliente)
        print(self.centrocosto)
        print(self.razonsocial)
        print(self.cargo)
        print(self.requierefirma)
        print(self.capacitacion)
        print(self.estado)
        print("\n")


def procesaArchivo(archivo):

    with open(archivo, "r", encoding="utf-8") as f:
       lista = list(csv.reader(f, delimiter=','))
    i=0
    trabajador=[]
    for row in lista:
        j=0
        for col in row: 
            if j==2:
                if i==0:
                    columnas.append(col)
                else:
                    trabajador.append(col)
            elif j==3:
                if i==0:
                    columnas.append(col)
                else:
                    trabajador.append(col)
            elif j==5:
                if i==0:
                    columnas.append(col)
                else:
                    trabajador.append(col)
            elif j==6:
                if i==0:
                    columnas.append(col)
                    columnas.append("RAZON SOCIAL")
                else:
                    trabajador.append(col)
                    ceco=col
                    aux=re.findall('\d+',ceco).pop()
                    trabajador.append(diccionario[aux])
            elif j==9:
                if i==0:
                    columnas.append(col)
                else:
                    trabajador.append(col)
            elif j==13:
                if i==0:
                    columnas.append(col)
                else:
                    trabajador.append(col)   
            elif j>=15:
                if i==0:
                    capacitacion[j]=col
                else:
                    if col=="PENDIENTE" or col=="CERRADO":
                        trabajador.append(capacitacion[j])
                        trabajador.append(col)                  
            j=j+1                   
        i=i+1
        if i>0 and len(trabajador)>0:
            trabajadores.append(trabajador)
            trabajador=[]
    i=0
    acum=0
    for worker in trabajadores:
        resto=0
        resto=int((len(worker)-7)/2)
        n=0
        while n <= resto-1:
            aux=Arbeiter(trabajadores[i][0],trabajadores[i][1],trabajadores[i][2],trabajadores[i][3],trabajadores[i][4],trabajadores[i][5],trabajadores[i][6],trabajadores[i][6+(2*n+1)],trabajadores[i][8+2*n])
            total.append(aux)
            acum=acum+1
            n=n+1
        i=i+1
    return total

def muestraTrabajadores(listado,n):
    k=0
    for item in listado:
        print(k+1)
        item.show()
        k=k+1
        if k==n:
            break
    




# muestraTrabajadores(procesaArchivo("Subconjunto(50).csv"),11)








