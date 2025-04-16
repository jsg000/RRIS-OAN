'''
Programa creado por Javier Sanchez Gonzalez jsanchezg@unal.edu.co
Para el interferometro de tres elementos PhAraON-OAN, su funcion es ubicar las antenas en las coordenadas deseadas 
'''
import serial
import time    # para el manejo de eventos de tiempo, nativa de Python

# funciones para enviar y recibir mensajes en formato de texto,
# codificado en UTF-8
# los mensajes utilizan como terminador un caracter de final de línea '\n'
def encode_send(ser, texto):
    enc = f'{texto}\n'.encode('UTF-8')
    ser.write(enc)

# Esquema básico para request-response
# El código utilizado en Arduino es: serial-comm.ino

# 1. Inicializa el puerto de comunicación y espera a que esté listo
serialport = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(0.1)   # tiempo de espera recomendado: 100 ms
while True:

    # 2. Preparamos el mensaje a ser transmitido
    print('Intrucciones de orientacion:acimut + dirige a Oriente,altura + dirige a Norte, la estrella polar esta en 63 grados')
    print("Altura en angulo decimal")
    altang = input('altura: ')
    altang = int(altang)
    print('Acimut en angulo decimal')
    aciang = input('acimut: ')
    aciang = int(aciang)
    paso = 0.03
    pasoalt = 0.015
    val_0 = (altang/pasoalt)
    val_1 = (aciang/paso)
    message_to_serial = str(val_0) + ' ' + str(val_1)+'\n'

# 3. Enviamos al puerto y esperamos la respuesta
    encode_send(serialport, message_to_serial)
    print(f'enviado: {message_to_serial}')
