# Se deberá leer el archivo y enviar los datos cada 30 segundos en formato json
# La cantidad de monedas en el archivo CSV puede ser variable (no siempre son 3 monedas)
# Capturar la signal SIGINT para salir del proceso de forma ordenada.
# El programa leerá la ruta del archivo CSV desde un archivo config.txt


# El archivo csv contiene:
#       id,nombre,compra,venta
#       1,Dolar,58.63,61.61
#       2,Euro,65.12,68.93
#       3,Real,13.45,14.23


import socket
import json
import os
import sys
import csv
import time
import signal


class MyHndlr(Exception):
    pass


def handler(sig, frame):
    raise MyHndlr


class precioMoneda():

    def __init__(self):
        """Constructor para incializar variables internas a la clase"""
        
        # Lista encabezado para armar el diccionario de JSON
        self.encabezado = ["id", "name", "value1", "value2"]
       
        self.precios = []
        self.preciosAEnviar = []
        
    def abrir(self, path):
        """Abrir el archivo CSV"""
        with open(path) as cfg:
            pathcsv = cfg.readline()
            self.f = open(pathcsv, newline="")
            self.reader = csv.reader(self.f)
        
        # Guardar el encabezado en una lista.
        self.linea = list(self.reader.__next__())

    def cerrar(self):
        """Cerrar el archivo"""

        self.f.close()
    
    def obtenerPrecios(self):
        """Lee los precios del archivo csv y los devuelve como JSON"""       

        for i, line in enumerate(self.reader):

            self.linea = list(line) # Linea leida del CSV
            self.lineaOrdenada = [self.linea[0], self.linea[1], self.linea[2], self.linea[3]] # Ordenar los precios
        
            # Arma diccionario {"id": 1, "name":"dolar", "value1":"100", "value2":"95" }
            self.precioDict = dict(zip(self.encabezado, self.lineaOrdenada)) 
        
            # Lista de los diccionarios de precio
            self.precios.append(self.precioDict) 

            # JSON de los diccionarios de precios
            self.preciosAEnviar = json.dumps(self.precios, indent=4)      
      
        return self.preciosAEnviar

        
class main():

    def __init__(self):
        pass

    def main(self):
        signal.signal(signal.SIGINT, handler)

        port = 10000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Escribiendo puerto "+str(port)+"...")
       
        cotizacion = precioMoneda()
        cotizacion.abrir("config.txt")   
        msg = bytes(cotizacion.obtenerPrecios(), "UTF-8")
        
        s.sendto(msg, ("localhost", port))
        

m = main()

try:
    while True:
        m.main()
        time.sleep(30)

except MyHndlr as e:
    print("Cerrando programa")
    sys.exit()


