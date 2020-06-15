import tkinter as tk

from Juego.Tipos import Casilla as TCasilla
from Juego.Posicion import Posicion

class Casilla():

    def __init__(self,canvas,posicion,tipo):
        self.__canvas = canvas
        self.__tipo = tipo
        self.__lineas = []
        self.__circulo = None
        self.__generar_lineas(posicion)

    def __generar_lineas(self,posicion):

        if self.__tipo == TCasilla.ATACADA:
            color = 'red'
        elif self.__tipo == TCasilla.DEFENDIDA:
            color = 'green' 
        elif self.__tipo == TCasilla.AMENAZADA:
            color = 'grey'
        else:
            color = 'blue'

        posicion_en_pantalla = posicion.calcular_posicion_en_pantalla()
        fila_inicial = posicion_en_pantalla.fila + 7
        fila_final = posicion_en_pantalla.fila + 97
        columna_inicial = posicion_en_pantalla.columna + 5
        columna_final = posicion_en_pantalla.columna + 95
        
        tmp_linea = self.__canvas.create_line(columna_inicial,fila_inicial,columna_inicial,fila_final,width=2,fill=color)
        self.__lineas.append(tmp_linea)

        tmp_linea = self.__canvas.create_line(columna_inicial,fila_inicial,columna_final,fila_inicial,width=2,fill=color)
        self.__lineas.append(tmp_linea)
        
        tmp_linea = self.__canvas.create_line(columna_final,fila_inicial,columna_final,fila_final,width=2,fill=color)
        self.__lineas.append(tmp_linea)
        
        tmp_linea = self.__canvas.create_line(columna_final,fila_final,columna_inicial,fila_final,width=2,fill=color)
        self.__lineas.append(tmp_linea)

        fila_inicial = fila_inicial + 32
        fila_final = fila_inicial + 26
        columna_inicial = columna_inicial + 32
        columna_final = columna_inicial + 26

        if self.__tipo == TCasilla.AMENAZADA:
            self.__circulo = self.__canvas.create_oval(columna_inicial,fila_inicial,columna_final,fila_final,width=2,fill=color)
    
    def eliminar_lineas(self):
        print("elimina lineas?")
        if len(self.__lineas) > 0:
            for linea in self.__lineas:
                self.__canvas.delete(linea)
        if self.__circulo != None:
            self.__canvas.delete(self.__circulo)