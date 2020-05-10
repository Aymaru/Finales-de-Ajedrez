import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from GUI import Carga
from Juego import *


def main(): 
    root = tk.Tk()
    app = Carga.Carga(root)
    root.mainloop()

def centrar(ventana):
    """Centra una ventana Tkinter
    """
    # Calculo del centro de la pantalla según el display.
    ventana.update_idletasks() # Actualiza desde el inicio en vez del update que lo hace despues del primer after
    # Dimension de la pantalla
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    # Dimensiones de la ventana de inicio
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2) -20
    ventana.geometry('{}x{}+{}+{}'.format(width, height, x, y)) # Ubico la pantalla
    return ventana

def leer_tablero(file):
    
    f = open(file,"r+")
    tablero = f.read()
    f.close()
    return tablero

if __name__ == '__main__':
    main()

#"C:/Users/ayma-93/Documents/TEC/2020 - Semestre I/Inteligencia Artificial/Proyectos/Finales de ajedrez/Finales de Ajedrez/Tableros/finalesCaso2.txt"
#"C:/Users/ayma-93/Documents/TEC/2020 - Semestre I/Inteligencia Artificial/Proyectos/Finales de ajedrez/Finales de Ajedrez/Tableros/tablero_inicial.txt"
#"/Tableros/tablero_inicial.txt"

##enrroque blancas  |    T   |   R   |  largo   |    T   |   R   | 
##                      7,0     7,4       ->        7,3     7,2
##                  |    T   |   R   |  corto   |    T   |   R   | 
##                      7,7     7,4       ->        7,5     7,6

##enrroque negras   |    T   |   R   |  largo   |    T   |   R   | 
##                      0,0     0,4       ->        0,3     0,2
##                  |    T   |   R   |  corto   |    T   |   R   | 
##                      0,7     0,4       ->        0,5     0,6
    
