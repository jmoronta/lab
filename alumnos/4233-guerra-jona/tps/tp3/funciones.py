#!/usr/bin/python3

import os
import sys 
import binascii

def abrir_archivo(file):
    '''Abre el archivo indicado en modo lectura'''
    fd = os.open(file, os.O_RDONLY)
    return fd

def crear_archivo(file):
    '''Crea el archivo indicado en modo escritura'''
    fd = os.open(file, os.O_WRONLY | os.O_CREAT)
    return fd

def leer_mensajes(mq, rgb_file, color):
    '''Leemos desde una cola de mensajes y guardamos en el archivo enviado'''
    msg = ""
    fd = crear_archivo(rgb_file)
    rgb_options = color.split(",")
    # print("procesando color: ", rgb_options[0])
    # print("procesando intensidad: ", rgb_options[1])
    while msg != "DONE":
        try:
            msg = mq.get()
            block = procesar_color(msg, rgb_options)
            os.write(fd, block)
        except TypeError as error:
            print("TypeError: {0}".format(error))
            #sys.exit(2)
        #finally:
        #    lock.release()

    os.close(fd)
    print("Proceso exitoso...") #os.getpid()

def procesar_color(bytes, color):
    '''Procesamos el bloque de bytes segun el color enviado'''
    if (color[0] == "R"):
        linea = procesar_rojo(bytes, color[1])
    elif (color[0] == "G"):
        linea = procesar_gris(bytes, color[1])
    else:
        linea = procesar_azul(bytes, color[1])
    return linea

def procesar_rojo(bytes, intensidad):
    #print('procesando rojo con intensidad: ', intensidad)

    # enter => 0A
    # primer byte => 28 

    # genero las posiciones que tengo q cambiar
    if(bytes[0] == 'P'):
        start=28
    else:
        start=0
    elem = start
    posiciones = []
    tope = len(bytes)
    while elem < tope:
        posiciones.append(elem)
        elem = elem+3
    #print(posiciones)

    #cambio mis colores
    contador=0
    linea=""
    for byte in bytes:
        if (contador in posiciones):
            h=binascii.b2a_hex(byte) # => str
            i = int(h, 16) # str to int
            result = i*int(intensidad)
            '''
            print('-------------------------------------')
            print('result value: ',result)
            print('result type: ',type(result))
            print('--------------convetimos-------------')
            print('hexa: ',hex(result)[2:])
            print('-------------------------------------')
            '''
            # TODO: este el es problema, debo pasar de INT a HEXA y despues a STR
            linea=linea+str(result) #[2:]
            #print(hex(result))
            #print(linea)
            #sys.exit(1)
        else:
            linea=linea+'FF' # TODO: en 0
        contador = contador+1

    #return bytes
    return linea

def procesar_gris(bytes, intensidad):
    #print('procesando gris con intensidad: ', intensidad)

#    if(bytes[0] == 'P'):
#        start=28
#    else:
#        start=0
#    elem = start+1
#    posiciones = []
#    tope = len(bytes)
#    while elem < tope:
#        posiciones.append(elem)
#        elem = elem+3
#    print('GRIS')
#    print(posiciones)
    #sys.exit(1)
    return bytes

def procesar_azul(bytes, intensidad):
    #print('procesando azul con intensidad: ', intensidad)

#    if(bytes[0] == 'P'):
#        start=28
#    else:
#        start=0
#    elem = start+2
#    posiciones = []
#    tope = len(bytes)
#    while elem < tope:
#        posiciones.append(elem)
#        elem = elem+3
#    print('AZUL')
#    print(posiciones)
    #sys.exit(1)
    return bytes