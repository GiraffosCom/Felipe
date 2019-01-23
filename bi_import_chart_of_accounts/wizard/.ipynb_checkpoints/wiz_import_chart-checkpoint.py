# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
import tempfile
import binascii
import xlrd
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io
import re

try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

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
    
    def getRut(self):
        return self.rut
    def getNombre(self):
        return self.nombre
    def getCliente(self):
        return self.cliente
    def getCentroCosto(self):
        return self.centrocosto
    def getRazonSocial(self):
        return self.razonsocial
    def getCargo(self):
        return self.cargo
    def getFirma(self):
        return self.requierefirma
    def getCapacitacion(self):
        return self.capacitacion
    def getEstado(self):
        return self.estado

def limpiarCeco(palabra):
    delimitador=" ("
    n=palabra.find(delimitador)
    return palabra[0:n]

def procesaArchivo(archivo):
    i=0
    total=[]
    trabajador=[]
    lista = archivo
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

    lista_reducida=[]
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
                    trabajador.append(limpiarCeco(col))
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
    
    for worker in trabajadores:
        resto=0
        resto=int((len(worker)-7)/2)
        n=0
        while n <= resto-1:
            aux=Arbeiter(trabajadores[i][0],trabajadores[i][1],trabajadores[i][2],trabajadores[i][3],trabajadores[i][4],trabajadores[i][5],trabajadores[i][6],trabajadores[i][6+(2*n+1)],trabajadores[i][8+2*n])
            total.append(aux)
            
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

def eliminaRegistros(self):
		records=self.env['x_registro'].search([])
		for elemento in records:
			elemento.unlink()

def creaRegistros(self,listado):
		o_registro=self.env['x_registro']
		for trabajador in listado:
			data={
				'x_name': trabajador.getNombre(),
				'x_studio_rut': trabajador.getRut(),
				'x_studio_cliente': trabajador.getCliente(),
				'x_studio_centro_costo': trabajador.getCentroCosto(),
				'x_studio_razon_social': trabajador.getRazonSocial(),
				'x_studio_cargo': trabajador.getCargo(),
				'x_studio_requiere_firma':trabajador.getFirma(),
				'x_studio_capacitacion_1':trabajador.getCapacitacion(),
				'x_studio_estado':trabajador.getEstado(),}
			o_registro.create(data)

class ImportChartAccount(models.TransientModel):
	_name = "import.chart.account"

	File_slect = fields.Binary(string="Seleccionar archivo")
	import_option = fields.Selection([('csv', 'Archivo CSV')],string='Tipo',default='csv')

	@api.multi
	def imoport_file(self):
		if self.import_option == 'csv':
			try:
				csv_data = base64.b64decode(self.File_slect)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				values = {}
				csv_reader = csv.reader(data_file, delimiter=';')
				file_reader.extend(csv_reader)
			except:

				raise Warning(_("Archivo inválido"))

			eliminaRegistros(self)
			creaRegistros(self,procesaArchivo(file_reader))
		else:
			raise Warning(_("Por favor seleccione un archivo CSV separado por ';' " ))

		return True
