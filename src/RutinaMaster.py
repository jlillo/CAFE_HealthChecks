# -*- coding: utf-8 -*-
"""
@author: Jesús Rentero Bonilla y Jorge Lillo-Box
Rutina Master.
Objetivo: Ejecutar cada una de las rutinas de manera automática.
          Esto se realizará sobre el directorio que la rutina Master reciba
          por parámetros. La rutina master se encargará de ejecutar las
          siguientes rutinas:
          - Rutina 01: ARC-Spots. Medir las posiciones de los spots de una imagen arco.
          - Rutina 02: Posición e intensidad del flat.
                       Determinará la posición de las órdenes por columnas en el CCD.
          - Rutina 03: Degradación del CCD (No se ejecutará para espectros no reducidos)
          - Rutina 04: Nivel de BIAS.
          - Rutina 05: Eficiencia de la noche. (tiempo exposicion/tiempo empleado)
tmp
"""
# Para instalar ephem: pip install pyephem
import sys
from astropy.io import fits
import os.path
from os import system
from os import listdir
from termcolor import colored
import Rutina01_v01
import Rutina02_v01
import Rutina04_v01
import Rutina05_v01
from paths_Rutinas import *

# """
# Carpeta de almacenamiento de resultados
# """
# HOME_FOLDER = "/Users/lillo_box/00_Instrumentation/CAFE2/CAFE_HealthChecks"
# 
# """
# Carpeta de almacenamiento de resultados
# """
# TMP_RESULTS = HOME_FOLDER+"/tmp_Results"
# MASTER_RESULTS = HOME_FOLDER+"/master_Results"
# 
# """
# Carpeta de datos
# """
# DATA_FOLDER = HOME_FOLDER+"/data"
# DATA_FOLDER_ORIG = "/Users/lillo_box/00_Instrumentation/CAFE2/data_HealthCheck_tests"
# 
# """
# Constantes para almacenar la ruta de los ficheros arco y flats que tomamos como referencia
# """
# ARCO_REF = HOME_FOLDER+"/ReferenceFiles/newgrat_0004.fits"
# FLAT_REF = HOME_FOLDER+"/ReferenceFiles/newgrat_0005.fits"
# 
# """
# Constantes donde almacenamos los nombres de los ficheros que contienen el listado
# de ficheros arco,flat y bias 
# """
# FICH_ARCO = HOME_FOLDER+"/auxiliar/arcoFits.txt"
# FICH_FLAT = HOME_FOLDER+"/auxiliar/flatFits.txt"
# FICH_BIAS = HOME_FOLDER+"/auxiliar/biasFits.txt"


"""
Funcion que se encarga de generar las listas de ficheros para arco, flats y bias
del directorio que se recibe por parámetro 
"""
def generarListaFicheros():
    # Obtenemos el directorio donde se encuentran todos los ficheros
    direct=DATA_FOLDER+'/'+sys.argv[1]
    # Definimos un directorio auxiliar de trabajo
    directAux=direct+'_aux'
    
    # Realizamos una copia del directorio con el que vamos a trabajar
    # En linux
    #system('cp -r '+direct+' '+directAux)
    directAux=direct
    
    #Creamos ficheros para arco, flat y bias
    arcoFits=open(FICH_ARCO,"w")
    flatFits=open(FICH_FLAT,"w")
    biasFits=open(FICH_BIAS,"w")
    
    # Recorremos el directorio
    for fichero in listdir(directAux):
        if os.path.isfile(directAux+"/"+fichero) and fichero.endswith(".fits"):
            rutaFich=directAux+"/"+fichero
            # Abrimos el fichero
            f=fits.open(rutaFich)
            # Obtenemos el tipo de fichero que estamos tratando
            objeto=f[0].header["OBJECT"].lower()
            if objeto[0]=='[':
                tipo=objeto[:objeto.index(']')+1]
            else:
                tipo='[science]'
            #print "%s - %s"%(rutaFich,tipo)
            #Clasificamos los ficheros segun su tipo y creamos una lista de ficheros para cada tipo
            if tipo=='[arc]':
                arcoFits.write(rutaFich+"\n")
            elif tipo=='[flat]':
                flatFits.write(rutaFich+"\n")
            elif tipo=='[bias]':
                biasFits.write(rutaFich+"\n")
                    
            f.close()
    
    arcoFits.close()
    flatFits.close()
    biasFits.close()


"""
Función que se encarga de lanzar las rutinas 1 y 2
"""
def run_Rutina01_Rutina02(directorio,night):
    #Arrancamos la rutina 01. 
    print " "
    print "==================================="
    print "EJECUTANDO RUTINA 01: ARC-SPOTS ..."
    print "==================================="
    # Obtenemos la matriz de datos del fichero que cogemos como referencia
    print "Creando matriz de datos..."
    tbdata=Rutina01_v01.getMatrizDatos(ARCO_REF)
    if 1:
		# Generamos el fichero input_spot.txt que utilizaremos para el estudio
		print "Creando fichero input_spot.txt..."
		Rutina01_v01.generarInputSpot(HOME_FOLDER+"/ReferenceFiles/spots.txt",tbdata)
		# Lanzamos la rutina generando para cada fichero arco un fichero de datos con los resultados
		print "Buscando spots en cada arco..."
		Rutina01_v01.rutina01Run(FICH_ARCO)
		#Rutina01_v01.promedioDistancias(FICH_ARCO)
		# Generamos el fichero Master de la primera rutina:
		print "Almacenando resultados en el fichero master..."
		Rutina01_v01.checkRutina01(FICH_ARCO)
		print "Generando plot de estabilidad de arcos de la noche..."
		Rutina01_v01.Plot1night(directorio,night)
    
    # Cargamos ajustes de la rutina02
    Rutina02_v01.cargarAjustes(FLAT_REF)
    # Lanzamos la rutina 02.
    print " "
    print "========================================================"
    print "EJECUTANDO RUTINA 02: Posición e intensidad del flat ..."
    print "========================================================"
    Rutina02_v01.rutina02Run(FICH_FLAT)
    


#Comprobamos que se ha introducido un parámetro al programa y que sea un directorio
if len(sys.argv)==2:
    if os.path.exists(DATA_FOLDER_ORIG+'/'+sys.argv[1]) and not os.path.isfile(DATA_FOLDER_ORIG+'/'+sys.argv[1]):
        print "... Copiando datos en carpeta temporal"
        os.system("cp -r "+DATA_FOLDER_ORIG+"/"+sys.argv[1]+" "+DATA_FOLDER+'/'+sys.argv[1])
        print "... Generando clasificacion y listas de ficheros"
        generarListaFicheros()
        
        run_Rutina01_Rutina02(DATA_FOLDER+'/',sys.argv[1])
        
        print " "
        print "==================================================="
        print "EJECUTANDO RUTINA 04: Control del nivel de BIAS ..."
        print "==================================================="
        Rutina04_v01.runRutina04(DATA_FOLDER+'/',sys.argv[1])

        print " "
        print "==========================================================="
        print "EJECUTANDO RUTINA 05: Calculando tiempos de observación ..."
        print "==========================================================="
        Rutina05_v01.runRutina05(DATA_FOLDER+'/',sys.argv[1])
        # Hacemos los plots
        Rutina01_v01.plotHistory()
        Rutina02_v01.plotHistory()
        Rutina04_v01.plotHistory()

        print " "
        print "... Eliminando carpetas y ficheros temporales"
        os.system("rm -rf "+DATA_FOLDER+'/'+sys.argv[1])
        os.system("rm -rf "+TMP_RESULTS+'/Rut01_dat/*.spot')
        os.system("rm -rf "+TMP_RESULTS+'/Rut02_dat/*_dat.txt')
        print "... Health Checks de CAFE 2.0 terminados :)"
    else:
        print "El directorio introducido no existe"
else:
    print "ERROR de SINTAXIS:"
    print "... El numero de parámetros es incorrecto."
    print "... Debes introducir el directorio de trabajo:"
    print "... SINTAXIS: python RutinaMaster.py [directorio]"

