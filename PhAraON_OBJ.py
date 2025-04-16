'''
Programa creado por Javier Sanchez Gonzalez jsanchezg@unal.edu.co
Para el interferometro de tres elementos PhAraON-OAN para seguir objetos fuera del sistema solar 
'''
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u
import time
import math
import serial
# funciones para enviar y recibir mensajes en formato de texto, codificado en UTF-8
# los mensajes utilizan como terminador un caracter de final de línea '\n'
def encode_send(ser, texto):
    enc = f'{texto}\n'.encode('UTF-8')
    ser.write(enc)
# 1. Inicializa el puerto de comunicación y espera a que esté listo
USBaltaz = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
# serialport = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(0.1)   # tiempo de espera recomendado: 100 ms
# 2. Preparamos el mensaje a ser transmitido
# Localiza en tiempo y espacio
OANUN = EarthLocation(lat=4.6397674*u.deg, lon=-74.0833258*u.deg, height=2560*u.m)
current_time = Time.now()
current_time_5 = Time.now()-10*u.s
# La estrella polar es la posicion inicial
altaz = AltAz(obstime=current_time, location=OANUN)
altaz_5 = AltAz(obstime=current_time_5, location=OANUN)
# El objetivo es el sol CYGNUS A, CASSIOPEIA A ,T CORONA BOREALIS
fuente = SkyCoord.from_name("CASSIOPEIA A", frame='icrs')
az_tel = round(fuente.transform_to(altaz_5).az.degree, 3)            # Azimut A
alt_tel = round(fuente.transform_to(altaz_5).alt.degree, 3)
Objalt = round(fuente.transform_to(altaz).alt.degree, 3)
Objaz = round(fuente.transform_to(altaz).az.degree, 3)
pasoalt = 0.015
paso = 0.03
altura_ = round((Objalt/pasoalt)*-1, 1)
azimut_ = round((Objaz/paso), 1)
print('el objetivo es=', current_time, 'Alt=', Objalt, 'az=', Objaz)
print('el objetivo es=', current_time_5, 'Alt=', alt_tel, 'az=', az_tel)
ubicacion = str(altura_)+' '+str(azimut_)
encode_send(USBaltaz, ubicacion)
print(f'enviado: {ubicacion}')
time.sleep(15)
while (Objalt != alt_tel) | (Objaz != az_tel):
    current_time_5 = Time.now()-10*u.s
    altaz_Obj = AltAz(obstime=current_time_5, location=OANUN)
    Obj_alt = round(fuente.transform_to(altaz_Obj).alt.degree, 3)
    Obj_az = round(fuente.transform_to(altaz_Obj).az.degree, 3)
    # Seguimiento en altura cada segundo
    if(Obj_alt-alt_tel > 1.0):  # sube
        paiz = math.trunc(abs(Obj_alt-alt_tel))
        alt_tel = round(alt_tel+paiz, 3)
        alt_i = str('-')+''+str(paiz/pasoalt)+' '
    elif(alt_tel-Obj_alt > 1.0):  # baja
        pade = math.trunc(abs(Obj_alt-alt_tel))
        alt_tel = round(alt_tel-1.00, 3)
        alt_i = str(pade/pasoalt)+' '
        # Seguimiento en azimut cada segundo
    else:
        alt_i = str(0)+' '
    if(Obj_az-az_tel > 1.0):
        pasu = math.trunc(abs(Obj_az-az_tel))
        az_tel = round(az_tel+1.00, 3)
        az_i = str(pasu/paso)+'\n'
    elif(az_tel-Obj_az > 1.0):
        pano = math.trunc(abs(Obj_az-az_tel))
        az_tel = round(az_tel-1.00, 3)
        az_i = str('-')+''+str(pano/paso)+'\n'
    else:
        az_i = str(0)+'\n'
    # print(alt_i,az_i)
    print(Obj_alt, alt_tel)
    print(Obj_az, az_tel)
    movimiento_i = str(alt_i)+' '+str(az_i)
    encode_send(USBaltaz, movimiento_i)
# 4. Procesamos la respuesta
    print(f'enviado: {movimiento_i}')
    time.sleep(10)
