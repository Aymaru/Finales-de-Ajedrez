import Juego
import archivos

file = "tableros_para_jugar.txt" 

partidas = archivos.leer_partidas(file)
juego1 = Juego.Juego("B","N","B",partidas[0])
juego1.tablero.imprimir_tablero()

posibles_movimientos = juego1.tablero.generar_posibles_movimientos()
for movimiento in posibles_movimientos:
    movimiento.imprimir_movimiento()
#posibles_movimientos
