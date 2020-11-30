#!/usr/bin/python3
import os
import sys 
import binascii
import array


def abrir_archivo(file):
    '''Abre el archivo indicado en modo lectura'''
    try :
    	fd = os.open(file, os.O_RDONLY)
    	return fd
    except FileNotFoundError:
    	return 0
	
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

def procesar_mimetype(consulta):
    dic={"text":"text/plain","jpg":"image/jpeg","ppm":"image/x-portable-pixmap","html":"text/html","pdf":"application/pdf","ico":"image/x-image"}
    
    if consulta == "" :
    	tipo = 0
    	return tipo
    
    else :
    	tipo=dic[consulta]
    return tipo
    	

def cambiar_colores_red(self, lista, intensidad):
        self.lista = lista
        x = 0
        for i in range(0, len(lista), 3):
            self.lista[i] = int(float(self.lista[i]) * float(intensidad))
            x = i+2
            if self.lista[i] > 255:
                self.lista[i] = 255
            if x-1 < len(lista):
                self.lista[i + 1] = 0
            if x < len(lista):
                self.lista[i + 2] = 0
        return self.lista
def cambiar_colores_green(self, lista, intensidad):
        self.lista = lista
        x = 0
        for i in range(0, len(lista), 3):
            x = i+2
            if x-1 < len(lista):
                self.lista[i + 1] = int(float(self.lista[i+1]) *
                                        float(intensidad))
                if self.lista[i + 1] > 255:
                    self.lista[i + 1] = 255
            self.lista[i] = 0
            if x < len(lista):
                self.lista[i + 2] = 0
        return self.lista
def cambiar_colores_blue(self, lista, intensidad):
        self.lista = lista
        for i in range(0, len(lista), 3):
            x = i+2
            if x < len(lista):
                self.lista[i + 2] = int(float(self.lista[i + 2]) *
                                        float(intensidad))
                if self.lista[i + 2] > 255:
                    self.lista[i + 2] = 255
            if x-1 < len(lista):
                self.lista[i + 1] = 0
            self.lista[i] = 0
        
        return self.lista
           
def espejado(encabezado, queuee, width, height):
    imagee = []
    image = []
    imagene = []
    cuerpo = b''
    while True:
        mensaje = queuee.get()
        if mensaje == "Terminamos":
            break
        else:
            cuerpo = cuerpo + mensaje
    cuerpo_c = [i for i in cuerpo]
    j = 0
    for i in range(height):
        for n in range(width):
            for c in range(3):
                valor = int(float(cuerpo_c[j]))
                imagene.append(valor)
                j += 1
            imagee.append(imagene)
            imagene = []
            imagee.reverse()
            image.extend(imagee[n])
    image_e = array.array('B', image)
    with open('espejado.ppm', 'wb') as f:
        f.write(bytearray(encabezado, 'ascii'))
        image_e.tofile(f)

