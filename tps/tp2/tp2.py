#!/usr/bin/python3
import os
import argparse
import array
import concurrent.futures as fut
import threading
from time import time

global reading
barrier = threading.Barrier(4)
lock = threading.Lock()


def cambiarA_LSB(byte, bit):
    if byte % 2 != bit:
        if bit == 1:
            byte += 1
        else:
            byte -= 1

    return byte


def modificar(color, total_bytes, cambio, message):
    global reading

    bits = [message[i] for i in range(color, len(message), 3)]
    written = 0
    while written < total_bytes:

        written = len(reading)

        # modifican bytes y guardan en lista
        while cambio != [] and cambio[0] < written:

            lock.acquire()

            index_to_change = cambio.pop(0)
            reading[index_to_change] = cambiarA_LSB(reading[index_to_change], int(bits.pop(0)))
            lock.release()

        barrier.wait()
def cabecera(fd):
    lines = os.read(fd, 100).splitlines()
    comments = []
    header_end = 0
    for line in lines:
        if line == b"P6":
            header_end += len(line) + 1
        elif line[0] == ord("#"):
            comments.append(line)
            header_end += len(line) + 1
        elif len(line.split()) == 2:
            words = line.split()
            width = int(words[0])
            height = int(words[1])
            header_end += len(line) + 1
        else:
            max_c = int(line)
            header_end += len(line) + 1
            break

    return header_end, width, height, max_c, comments


def crearcabecera(width, height, max_c, comments):
    return "P6\n" + comments + "\n" + str(width) + " " + str(height) + "\n" + str(max_c) + "\n"

# main del programa
def main():
    inicio = time()

    global reading
    reading = []

    # argumentos
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", type=str, required=True,
                        help="ppm should be")
    parser.add_argument("-m", "--message", type=str, required=True,
                        help="file")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="file")
    parser.add_argument("-s", "--size", type=int, default=1024,
                        help="size")
    parser.add_argument("-e", "--offset", type=int, required=True,
                        help="interleave pixels")
    parser.add_argument("-i", "--interleave", type=int, required=True,
                        help="interleave pixels")

    args = parser.parse_args()


    if not args.file.endswith(".ppm"):
        raise print("la imagen debe ser con la extension ppm") 

    # determino el path del script
    path = os.path.dirname(__file__)
    #print(path)
    # determino la longitud de la imagen
    L_file = os.path.getsize(path + args.file)

    # determino el mensaje a escribir y su longitud
    with open(path + args.message, "rb") as archivo:
        message = archivo.read()
        L_TOTAL = len(message)

    x = []
    for i in message:
        bit = bin(i)[2:]
        while len(bit) < 8:
            bit = "0" + bit
        x.append(bit)

    message = "".join(x)

    # abro la imagen
    fd = os.open(path + args.file, os.O_RDONLY)

    # leo el header de la imagen
    header_end, width, height, max_c, comments = cabecera(fd)

    # muevo el puntero al primer pixel del cuerpo modificar
    os.lseek(fd, header_end, 0)

    # inserto el comentario con los datos de la codificacion
    comments = "#UMCOMPU2 " + str(args.offset) + " " + str(args.interleave) + " " + str(L_TOTAL)

    # crea el archivo imagen solo con el header
    wfd = os.open(path + args.output, os.O_WRONLY | os.O_CREAT)
    N_header = crearcabecera(width, height, max_c, comments)
    L_header = len(N_header)
    os.close(wfd)

    # determina pixels a modificar
    # Los indices de los pixels son en relacion al inicio del raster, que es donde se va a empezar a leer
    modify_indexes_R = []
    c = 0
    for pixel in range(args.offset*3, L_file - header_end, args.interleave*3):

        modify_indexes_R.append(pixel + c)
        c += 1
        if c == 3:
            c = 0

    modify_indexes_R = modify_indexes_R[:len(message)]

    r = [modify_indexes_R[i] for i in range(0, len(modify_indexes_R), 3)]
    g = [modify_indexes_R[i] for i in range(1, len(modify_indexes_R), 3)]
    b = [modify_indexes_R[i] for i in range(2, len(modify_indexes_R), 3)]

    indexes = (r, g, b)

    # lanza hilos
    hilos = fut.ThreadPoolExecutor(max_workers=3)
    [hilos.submit(modificar, i, width * height * 3, indexes[i], message) for i in range(3)]

    output = open(path + args.output, "wb", os.O_CREAT)
    output.write(bytearray(N_header, 'ascii'))

    # lee imagen
    written = 0
    while written < (width * height * 3):
        lock.acquire()
        reading += [i for i in os.read(fd, args.size)]
        lock.release()
        written = len(reading)
        barrier.wait()

    # escribe la imagen
    if reading:
        image = array.array('B', reading)
        image.tofile(output)
    try:
        barrier.wait(0.1)
    except threading.BrokenBarrierError:
        pass

    output.close()
    print("Terminamos, inicio del raster es:",L_header, "y el tamaño del mensaje es:",L_TOTAL)
    print(str(time()-inicio)[:4], "segundos")

if __name__ == "__main__":
    main()

