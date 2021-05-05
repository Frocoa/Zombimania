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
        self.isInfected = True # Estado de enfermedad del jugador
        self.deathRolls = 0 # cantidad de veces que el virus "afecta" al jugador
        self.spriteCooldown = 0.08
        self.spriteIndex = 0
        self.timePassed = 0
        self.t0 = 0
        self.t1 = 0

    def set_model(self, new_model):
        # Se obtiene una referencia a uno nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller
    
    def nextSpriteIndex(self):
        if self.timePassed >= self.spriteCooldown:
            self.spriteIndex = (self.spriteIndex+1)%6
            self.t0 = self.t1
            return self.spriteIndex
        else:
            return self.spriteIndex

    def update(self, delta):
        self.t1 = glfw.get_time()
        self.timePassed = self.t1 - self.t0

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
        # Se hace una tirada de infeccion cada frame para ver cuanto aguanta el player
        if self.isInfected == True and self.isAlive:
            if(rand.uniform(0.0,100.0) >= 99.9):
                self.deathRolls += 1
        # Si la infeccion avanzo demasiado entonces el personaje muere y se transforma en un zombi
        if self.deathRolls >= 7:
            self.isAlive = False

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.sizeX, self.sizeY, 1)])

    def collision(self, cargas):
        # Funcion para detectar las colisiones con las cargas

        # Se recorren las cargas 
        for carga in cargas:
            # si la distancia a la carga es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+carga.radio)**2 > ((self.pos[0]- carga.pos[0])**2 + (self.pos[1]-carga.pos[1])**2):
                #self.isAlive = False
                return
        
class Zombie():
    # Clase de los Zombis
    def __init__(self, posX, posY, size, speed, goingUpwards):
        self.pos = [posX, posY]
        self.radio = 0.02
        self.size = size
        self.model = None
        self.speed = speed
        self.goingUpwards = goingUpwards
        self.shouldBeRemoved = False
        self.spriteCooldown = 0.05/np.absolute(speed)
        self.spriteIndex = 0
        self.t0 = 0
        self.t1 = 0

        if (self.goingUpwards):
            self.pos[1] = -self.pos[1]
            self.speed = - self.speed

    def set_model(self, new_model):
        self.model = new_model
    
    def checkShouldBeRemoved(self):
        if np.absolute(self.pos)[1] >= 1.5:
            self.shouldBeRemoved = True

    def remove(self, zombieGroup, zombieList):
        self.model.childs = []
        zombieGroup.childs.pop(zombieGroup.childs.index(self.model))
        zombieList.pop(zombieList.index(self))
        self.model.clear()


    def update(self):
        # Se posiciona el nodo referenciado
        self.t1 = glfw.get_time()

        deltaSpriteChange = self.t1 - self.t0

        if deltaSpriteChange >= self.spriteCooldown:
            self.spriteIndex = (self.spriteIndex + 1) % 7
            self.t0 = self.t1

        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size*1.4, 1)])
        self.checkShouldBeRemoved()



class Human():
    # CLase para los humanos
    def __init__(self, posX, posY, size, speed, goingUpwards, isInfected):
        self.pos = [posX, posY]
        self.radio = 0.02
        self.size = size
        self.speed = speed
        self.isInfected = isInfected
        self.goingUpwards = goingUpwards
        self.model = None

        if (self.goingUpwards):
            self.pos[1] = -self.pos[1]

    def set_model(self, new_model):
        # Se le pone un modelo 
        self.model = new_model

    def update(self):
        # Se posiciona el nodo referenciado
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size*2, 1)])