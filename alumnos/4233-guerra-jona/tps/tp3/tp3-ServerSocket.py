#!/usr/bin/python3

import os
import sys
import argparse
import multiprocessing
import funciones as fc
import socketserver

class servidor(socketserver.ForkingTCPServer):
    def __init__(self,server_address,RequestHandlerClass,tamano,directorio):
        socketserver.ForkingTCPServer.__init__(self,server_address,RequestHandlerClass)
        socketserver.allow_reuse_address = True
        self.tamano = tamano
        self.directorio = directorio


class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            dic={"text":"text/plain","jpg":"image/jpeg","ppm":"image/x-portable-pixmap","html":"text/html","pdf":"application/pdf"}
            directorio = self.server.directorio
            tamano = self.server.tamano
            self.data = self.request.recv(1024)
            encabezado = self.data.decode().splitlines()[0]
            if encabezado.split()[1]== False:
                archivo = encabezado.split()[0]
            archivo = encabezado.split()[1]
            #extension = archivo.split('.')[1]
            #print(extension)
            if archivo == '/':
                archivo ='/index.html'
                extension='html'
            else: 
                #archivo = encabezado.split()[1] 
                extension= archivo.split('.')[1]
            #if os.path.isfile(archivo)== False:
            #    archivo = './400error.html'
            solicitud=directorio+archivo 
            print(solicitud)
            fd=fc.abrir_archivo(solicitud)
            if os.path.isfile(fd)  == False:
                header =bytearray("HTTP/1.1 404 error\r\n Content-Type:"+ dic[extension] +" \r\nContent-length: \r\n\r\n",'utf8')
                body   = "<html><head><meta<title>Mi pagina de prueba</title></head><body><p>Hola Mundo todo bien</p></body></html>"
            print(dic[extension])
            header =bytearray("HTTP/1.1 200 OK\r\n Content-Type:"+ dic[extension] +" \r\nContent-length: \r\n\r\n",'utf8')
            body = os.read(fd,tamano)
            respuesta = header + body
            self.request.sendall(respuesta)

if __name__ == "__main__":
    HOST="0.0.0.0"
    parser = argparse.ArgumentParser(description='Arrays')
    parser.add_argument('-d', '--Documentroot Dir', action="store", dest="directorio", metavar="archivo origen", type=str, required=True, help="Archivo a procesar")
    parser.add_argument('-p', '--port', action="store", dest="puerto",type=int, help="Puerto")
    parser.add_argument('-s', '--size', action="store", dest="n_bytes", metavar="numero de bytes", type=int, required=True, help="Bloque de lectura")        
    args = parser.parse_args()
        #print(args)
    directorio= args.directorio
    puerto=args.puerto
    tamano=args.n_bytes
    with servidor((HOST,5000),Handler,tamano,directorio)as server:
       server.serve_forever()
