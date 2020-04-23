import pygame 
import numpy as np 
import time

pygame.init()

#ancho y alto de pantalla
width, height = 1000, 1000
#creacion de pantalla
screen = pygame.display.set_mode((width, height))
#color de fondo = casi negro, casi oscuro
bg = 25, 30, 25
screen.fill(bg)

#medidas de cuadricula
nxC, nyC = 50, 50
dimCW = width / nxC
dimCH = height / nyC

#estado de las celdas: vivas=1 , muertas= 0
gameState = np.zeros((nxC, nyC))
    #inicializacion del juego
gameState [1,1] = 1
gameState [3,1] = 1
gameState [3,2] = 1
gameState [2,1] = 1
gameState [4,1] = 1
gameState [5,2] = 1

#control de la ejecucion
pauseExect= False

#bucle de ejecucion
while True:
    """para evitar que se actualice celda por celda, 
    hacemos una copia para que se guarden todos los estados de las celdas"""
    newGameState = np.copy(gameState)
    #no saturar la pantalla
    screen.fill(bg)
    """dar respiro al programa """
    time.sleep(0.1)
    #registramos eventos del teclado y raton
    ev = pygame.event.get()

    for event in ev:
        # pausar el juego usando teclado
        if event.type== pygame.KEYDOWN:
            pauseExect = not pauseExect
        #mostrar las coordenadas de donde este el mouse
        mouseClick= pygame.mouse.get_pressed()
        #print(mouseClick)
        #dar nuevas coordenadas para las celdas vivas
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int (np.floor(posX / dimCW)), int (np.floor(posY / dimCH))
            #poder usar izquierdo del mouse para matar las celdas
            newGameState[celX, celY] = not mouseClick[2]

    #recorrer todas las celdas una por una
    for y in range(0, nxC):
        for x in range(0, nyC):
            #si no esta en pausa, ejecuta el juego
            if not pauseExect:
                #calculamos el numero de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + gameState[(x)   % nxC, (y-1) % nyC] + gameState[(x+1) % nxC, (y-1) % nyC] + gameState[(x-1) % nxC, (y)   % nyC] + gameState[(x+1) % nxC, (y)   % nyC] + gameState[(x-1) % nxC, (y+1) % nyC] + gameState[(x)   % nxC, (y+1) % nyC] + gameState[(x+1) % nxC, (y+1) % nyC]
            
                #regla 1: una celda muerta con 3 vecinas vivas, "revive"
                if gameState [x, y] == 0 and n_neigh == 3:
                    newGameState [x, y] = 1 #vivo

                #regla 2: una celda viva con menos de 2, o mas de 3 vecinas vivas, "muere"
                elif gameState [x, y] == 1 and n_neigh < 2 or n_neigh > 3:
                    newGameState [x, y] = 0 #c muere

            #dibujar el poligono e cada celda a dibujar
            poly = [((x)*dimCW, y*dimCH),
                    ((x+1)*dimCW, y*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]
            #dibujamos la celda para cada par x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (100, 100, 100), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    #actualizamos el estado del juego
    gameState = np.copy(newGameState)
    
    #actualiza la pantalla
    pygame.display.flip()
