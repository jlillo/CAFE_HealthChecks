# CAFE_HealthChecks

**Purpose**

Check the health of the CAFE instrument installed at the 2.2m telescope in CAHA
after its upgrade in April 2018.

**Usage**

This scripts are to be used by the CAHA personnel at the observatory machines.

The syntax is very simple:
python RutinaMaster.py YYMMDD

**Ownership**

These tools have been developed by Jesus Rentero Bonilla in the context of his Master 
Thesis at the Valencia International University, VIU under the supervision of 
Jorge Lillo-Box, who has also contributed to further improve the routines and adapt them
to be run at Calar Alto Observatory.

If you make use of any of the data included in this repository, please acknowledge us
with the proposed sentence: "This work uses part of the CAFE health checks developed by
Jesus Rentero Bonilla and Jorge Lillo-Box."

**Further instructions (in Spanish)**

Para que funcione correctamente la master:
- Se realizara una copia del directorio que contiene todas las imagenes realizadas en la noche en el directorio de trabajo.

Para que funcione la rutina 01:
- Debe haber un directorio Rut01_dat para almacenar los resultados.
- Debe tener la imagen arco de referencia que se elija.
- Debe tener el fichero de entrada spots.txt con las coordenadas de los spots.

Para que funcione la rutina 02:
- Debe haber un directorio Rut02_dat para almacenar los resultados.
- Debe tener la imagen flat de referencia que se elija.
- Debe estar en el mismo directorio que la rutina master el fichero "ordenes_input.txt"

Para que funcione la rutina 03:
- Debe haber un directorio Rut03_dat para almacenar los resultados.

Para que funcione la rutina 04:
- Debe haber un directorio Rut04_dat para almacenar los resultados.

Para que funcione la rutina 05:
- Debe haber un directorio Rut05_dat para almacenar los resultados.

