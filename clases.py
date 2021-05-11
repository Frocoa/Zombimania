""" Clases y objetos correspondiente al modelo"""

import glfw
import numpy as np
import grafica.transformations as tr
import random as rand

class Player():
    # Clase que contiene al modelo del player / auro
    def __init__(self, sizeX, sizeY):
        self.pos = [0,-0.65] # Posicion en el escenario
        self.vel = [0.8,0.8] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.sizeX = sizeX # Escala en x a aplicar al nodo
        self.sizeY = sizeY # Escala en y a aplicar al nodo 
        self.radio = 0.1 # distancia para realiozar los calculos de colision
        self.isAlive = True # Estado de salud del jugador
        self.isInfected = False # Estado de enfermedad del jugador
        self.time = 0 # tiempo actual
        
       
        #Sprite management
        self.spriteIndex = 0
        self.spriteTimePassed = 0
        self.spriteT0 = 0
        self.spriteCooldown = 0.08

        #Dash management
        self.dashCooldown = 3
        self.dashTimePassed = 0
        self.dashT0 = 0
        self.dashDuration = 0.4
        self.dashing = False
        self.dashingMoment = 0
        self.dashLeft = True
       
    # Manejo de la vuelta de carnero que puedo hacer el jugador
    def dash(self, delta):
        if(self.dashing == True):

            if self.dashLeft == True:
                self.dashingMoment += 15*delta
                if 0.1*self.dashingMoment*15 >= 6.28319:
                    self.dashing = False
                    self.dashingMoment = 0
                    return

                # se mantiene en los limites
                if self.pos[0] > -0.72:
                    self.pos[0] -= 1.7*delta
            else:
                self.dashingMoment -= 15*delta
                if 0.1*self.dashingMoment*15 <= -6.28319:
                    self.dashing = False
                    self.dashingMoment = 0
                    return

                #se mantiene en los limites
                if self.pos[0] < 0.72:
                    self.pos[0] += 1.7*delta        

            # se actualiza la posicion y rotacion del jugador
            self.model.transform = tr.matmul([tr.translate(self.pos[0],self.pos[1],0),
                                              tr.rotationZ(0.1*self.dashingMoment*15),
                                              tr.scale(self.sizeX, self.sizeY, 1)])

    def set_model(self, new_model):
        # Se obtiene una referencia a uno nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller
    
    # controla la velocidad de la animacion del jugador
    def nextSpriteIndex(self):
        # permite ir al siguiente sprite de la animacion si ha pasado el tiempo
        if self.spriteTimePassed >= self.spriteCooldown:
            self.spriteIndex = (self.spriteIndex+1)%6
            self.spriteT0 = self.time
            return self.spriteIndex
        else:
            return self.spriteIndex

    # revisa si la infeccion transforma en zombi al jugador
    def deathRoll(self, odds):
        if rand.uniform(0,1) <= odds and not self.controller.gameWon:
            self.isAlive = False

    def update(self, delta):

        # si se detecta la letra q, se da una voltereta a la izquierda
        if self.controller.is_q_pressed and self.dashTimePassed >= self.dashCooldown:
            self.dashing = True
            self.dashT0 = self.time  
            self.dashTimePassed = 0
            self.dashLeft = True

        # si se detecta la letra e, se da una voltereta a la derecha
        if self.controller.is_e_pressed and self.dashTimePassed >= self.dashCooldown:
            self.dashing = True
            self.dashT0 = self.time  
            self.dashTimePassed = 0
            self.dashLeft = False    

        # control del enfriamiento de la voltereta
        self.dash(delta)
        self.dashTimePassed = self.time - self.dashT0
        
        # control de la velocidad de la animacion de caminar
        self.time = glfw.get_time()
        self.spriteTimePassed = self.time - self.spriteT0

        # Si detecta la tecla [D] presionada se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] <= 0.72 and self.isAlive:
            self.pos[0] += self.vel[0] * delta
        # Si detecta la tecla [A] presionada se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] >= -0.72 and self.isAlive:
            self.pos[0] -= self.vel[0] * delta 
        # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] <= 1.0 and self.isAlive:
            self.pos[1] += self.vel[1] * delta
        # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] >= -0.92 and self.isAlive:
            self.pos[1] -= self.vel[1] * delta
        # Se le aplica la transformacion de traslado segun la posicion actual
        if not self.dashing:
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.sizeX, self.sizeY, 1)])


    def collision(self, zombieList, humanList):
        # Funcion para detectar las colisiones con los zombis

        # Se recorren todos los zombis 
        for zombie in zombieList:
            # si la distancia al zombie es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+zombie.radio)**2 > ((self.pos[0]- zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2):
                self.isAlive = False
                return

        # Se recorren todos los humanos
        for human in humanList:
            # si la distancia al humano es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+human.radio)**2 > ((self.pos[0]- human.pos[0])**2 + (self.pos[1]-human.pos[1])**2):
                # se contagia la infeccion
                if human.isInfected == True:
                    self.isInfected = True

    # verifica si el jugador esta en la salida
    def checkWin(self):
        if self.pos[1] >= 0.70 and self.pos[1] <= 1.1:
            if self.pos[0] >= -1.0 and self.pos[0] <= -0.68:
                self.controller.gameWon = True


class Zombie():
    # Clase de los Zombis
    def __init__(self, posX, posY, size, speed, goingUpwards):
        self.pos = [posX, posY] # posicion en el escenario
        self.radio = 0.02 # radio de colision
        self.size = size # tamaño del modelo
        self.model = None # modelo asociado al zombi
        self.speed = speed # velocidad a la que corre 
        self.goingUpwards = goingUpwards # el zombi va hacia arriba o hacia abajo
        self.shouldBeRemoved = False # el zombi esta fuera de los limites del juego
        self.spriteCooldown = 0.05/np.absolute(speed) # velocidad de la animacion del zombi
        self.spriteIndex = 0 # numero de sprite en el que va la animacion
        self.goingRight = False # el zombi va hacia la derecha o la izquierda
        self.spriteT0 = 0 # ultima vez que se cambio el sprite
        self.time = 0 # momento actual

        if (self.goingUpwards):
            self.pos[1] = -self.pos[1]
            self.speed = - self.speed

    def set_model(self, new_model):
        # se coloca un nodo como modelo del zombi
        self.model = new_model
    
    def checkShouldBeRemoved(self):
        # el zombi esperara a ser eliminado si se sale de los limites del juego
        if np.absolute(self.pos)[1] >= 1.5:
            self.shouldBeRemoved = True

    def remove(self, zombieGroup, zombieList):
        # elimina al zombi y libera memoria
        self.model.childs = []
        zombieGroup.childs.pop(zombieGroup.childs.index(self.model))
        zombieList.pop(zombieList.index(self))
        self.model.clear()

    def checkDirection(self):
        # maneja hacia donde va el zombi luego de ser instanciado
        if self.goingUpwards == False:
            if self.pos[0] >= 0.7:
                self.goingRight = False
        
            if self.pos[0] <= -0.7:
                self.goingRight = True 

        elif self.goingUpwards == True:
            if self.pos[0] >= 0.7:
                self.goingRight = True
        
            if self.pos[0] <= -0.7:
                self.goingRight = False

        if rand.uniform(0,1) <= 0.002:
            self.goingRight = not self.goingRight

    def collision(self, humanList):

        # se revisan los humanos
        for human in humanList:
            # si la distancia al humano es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+human.radio)**2 > ((self.pos[0]- human.pos[0])**2 + (self.pos[1]-human.pos[1])**2):
                # el zombi crece al comer
                self.size += 0.02
                self.radio += 0.01


    def update(self):
        self.time = glfw.get_time()

        deltaSpriteChange = self.time - self.spriteT0

        # manejo de la animacion
        if deltaSpriteChange >= self.spriteCooldown:
            self.spriteIndex = (self.spriteIndex + 1) % 7
            self.spriteT0 = self.time

        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size*1.4, 1)])
        self.checkShouldBeRemoved()
        self.checkDirection()


class Human():
    # CLase para los humanos
    def __init__(self, posX, posY, size, speed, goingUpwards, isInfected):
        self.pos = [posX, posY] # posicion en el escenario
        self.radio = 0.02 # radio de colision
        self.size = size # tamaño del modelo
        self.speed = speed # velocidad para desplazarse
        self.isInfected = isInfected # el humano esta enfermo
        self.isAlive = True # estado de salud del humano
        self.shouldBeRemoved = False # debe ser eliminado al salirse de los limites
        self.goingUpwards = goingUpwards # direccion inicial
        self.model = None # nodo asociado al modelo
        self.spriteCooldown = 0.05/np.absolute(speed) # velocidad de la animacion
        self.goingRight = True # caminar a izquierda o derecha
        self.spriteIndex = 0 # numero de sprite 
        self.spriteT0 = 0 # ultima vez que se cambio el sprite
        self.time = 0 # momento actual

        if (self.goingUpwards):
            self.pos[1] = -self.pos[1]
            self.speed = - self.speed

    def set_model(self, new_model):
        # Se le pone un modelo 
        self.model = new_model

    # se verifica si el humano se salio de los limites del mapa
    def checkShouldBeRemoved(self):
        if np.absolute(self.pos)[1] >= 1.5:
            self.shouldBeRemoved = True

    # verifica si la infeccion lo mata
    def deathRoll(self, odds):
        if rand.uniform(0,1) <= odds:
            self.isAlive = False

    def remove(self, humanGroup, humanList):
        self.model.childs = []
        humanGroup.childs.pop(humanGroup.childs.index(self.model))
        humanList.pop(humanList.index(self))
        self.model.clear()
    
    # maneja hacia donde va el humano
    def checkDirection(self):
        if self.goingUpwards == False:
            if self.pos[0] >= 0.7:
                self.goingRight = False
        
            if self.pos[0] <= -0.7:
                self.goingRight = True 

        elif self.goingUpwards == True:
            if self.pos[0] >= 0.7:
                self.goingRight = True
        
            if self.pos[0] <= -0.7:
                self.goingRight = False

        if rand.uniform(0,1) <= 0.008:
            self.goingRight = not self.goingRight      
    
    # revisa colisiones
    def collision(self, zombieList, humanList):
        # se recorren todos los zombis
        for zombie in zombieList:
            if (self.radio+zombie.radio)**2 > ((self.pos[0]- zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2):
                self.isAlive = False  #tocar a un zombi lo mata
        # se recorren los otros humanos        
        for human in humanList:
            if (self.radio+human.radio)**2 > ((self.pos[0]- human.pos[0])**2 + (self.pos[1]-human.pos[1])**2):
                if(human.isInfected == True):
                    self.isInfected = True   # tocar a un infectado lo contagia  

    def update(self):
        self.time = glfw.get_time()

        deltaSpriteChange = self.time - self.spriteT0

        if deltaSpriteChange >= self.spriteCooldown:
            self.spriteIndex = (self.spriteIndex + 1) % 6
            self.spriteT0 = self.time

        # Se posiciona el nodo referenciado
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0),
                                          tr.scale(self.size, self.size*2, 1)])
        self.checkShouldBeRemoved()
        self.checkDirection()

class Star():
#Clase para las estrellas que recuerda su nodo y posicion

    def __init__(self, posX, posY):
        self.pos = [posX, posY]
        self.model = None 

    def setModel(self,model):
        # se entrega un nodo como modelo
        self.model = model

    def getModel(self):
        # retorna el modelo
        return self.model    

    def getPosX(self):
        # retorna la posicion en x
        return self.pos[0]

    def getPosY(self):
        # retorna la posicion en y
        return self.pos[1]           