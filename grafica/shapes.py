
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

import math
import random as rand

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName

# retorna min_value si num < min_value, 
#max_value si num > max_value, num sino
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)


# shape de alas con discretizacion
def createWings(n):  #Al poner un n mas alto las alas parecen mas como de insecto

    vertices = [0.0, 0.0, 0.0,  0.8, 0.643, 0.24]

    indices = []
    
    for i in range(n-2):
        colorChange = rand.uniform(0,0.1) # para evitar un color demasiado plano
        i += 1
        vertices += [       #vertices                  #Color dorado aleatorio
                            -0.5,  0.5-i*0.5/n,  0.0,  0.8 + colorChange, 0.643 + colorChange, 0.24 + colorChange,
                    0.0 - (0.5)/i, 0.5-i*0.5/n,  0.0,  0.8 - colorChange, 0.643 - colorChange, 0.24 - colorChange,

                              0.5,  0.5-i*0.5/n, 0.0,  0.8 - colorChange, 0.643 - colorChange, 0.24 - colorChange,
                    0.0 + (0.5/i),  0.5-i*0.5/n, 0.0,  0.8 + colorChange, 0.643 + colorChange, 0.24 + colorChange,]

        indices += [ 
                1+4*(i-1), 2+4*(i-1), 0,
                3+4*(i-1), 4+4*(i-1), 0]

    return Shape(vertices, indices)                         

def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)

# retorna los vertices de la estrella dinamica
def movileStarVertices(t):
    cos = clamp(abs(math.cos(18*t)),0.45,0.65)
    sin = clamp(abs(math.sin(18*t)),0.45,0.65)
    vertices = [       #Vertices                       # Colores
                    -0.5 * cos,   -0.25 * cos,  0,   0.8, 0.8, 0.0,
                     0.5 * cos,   -0.25 * cos,  0,   0.9, 0.8, 0.0,
                           0.0,     0.5 * cos,  0,   0.8, 0.8, 0.0,
                    -0.5 * sin,    0.25 * sin,  0,   0.8, 0.8, 0.0,
                     0.5 * sin,    0.25 * sin,  0,   0.9, 0.8, 0.0,
                           0.0,    -0.5 * sin,  0,   0.9, 0.8, 0.0]
    return vertices            

# crea una estrella con vertices dinamicos
def createMovileStar(newVertices):
    indices = [ 0, 1, 2,
                3, 4, 5]
    return Shape(newVertices, indices)
                            
def createTextureQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0,  0, ny,
         0.5, -0.5, 0.0, nx, ny,
         0.5,  0.5, 0.0, nx, 0,
        -0.5,  0.5, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)

# Crea una figura con varios vertices con la textura de una calavera
def createTextureSkull():
    vertices = [
        -0.3666, 0.3666, 0.0, 0.0, 0,
        0.3666, 0.3666, 0.0, 0.6111, 0,
        -0.3666, -0.23, 0.0, 0.0, 1,
        0.3666, -0.23, 0.0, 0.6111, 1,

        -0.4333, 0.5, 0.0, 0.6666, 0.4444,
        -0.1666, 0.5, 0.0, 0.8888, 0.4444,
        -0.4333, 0.2333, 0.0, 0.6666, 0.8888,
        -0.1666, 0.2333, 0.0, 0.8888, 0.8888,
        
        0.1666, 0.5, 0.0, 0.6666, 0.4444,
        0.4333, 0.5, 0.0, 0.8888, 0.4444,
        0.1666, 0.2333, 0.0, 0.6666, 0.8888,
        0.4333, 0.2333, 0.0, 0.8888, 0.8888,

        -0.5, -0.09, 0.0, 0.6666, 0.4444,
        -0.2333, -0.09, 0.0, 0.8888, 0.4444,
        -0.5, -0.3566, 0.0, 0.6666, 0.8888,
        -0.2333, -0.3566, 0.0, 0.8888, 0.8888,

        0.2333, -0.09, 0.0, 0.6666, 0.4444,
        0.5, -0.09, 0.0, 0.8888, 0.4444,
        0.2333, -0.3566, 0.0, 0.6666, 0.8888,
        0.5, -0.3566, 0.0, 0.8888, 0.8888,

        -0.2333, -0.23, 0.0, 0.6111, 0,
        0.2333, -0.23, 0.0, 1, 0,
        -0.2333, -0.43, 0.0, 0.6111, 0.3333,
        0.2333, -0.43, 0.0, 1, 0.3333]

    indices = [
            0, 1, 2,
            2, 3, 1,
            4, 5, 6,
            6, 5, 7,
            8, 9, 10,
            10, 9, 11,
            12, 13, 14,
            14, 13, 15,
            16, 17, 18,
            18, 17, 19,
            20, 21, 22,
            22, 21, 23]

    return Shape(vertices, indices)        

def createMultiTextureQuad(xi, xf, yi, yf):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0, xi, yf,
         0.5, -0.5, 0.0, xf, yf,
         0.5,  0.5, 0.0, xf, yi,
        -0.5,  0.5, 0.0, xi, yi]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


########################################################
#Aqui se empiezan a crear un monton de shapes de letras#
########################################################

def createLetterG():
    vertices = [
    #   positions        colors
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #0
                0.5, 0.25,0.0,  0.0, 0.0, 0.0, #1
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0, #2
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #3
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0, #4
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #5
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0, #6
                -0.5, -0.25, 0.0,  0.0, 0.0, 0.0, #7
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #8
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0, #9
                0.5, 0.0, 0.0,  0.0, 0.0, 0.0, #10
                0.25, 0.0, 0.0,  0.0, 0.0, 0.0, #11
                0.0, 0.0, 0.0,  0.0, 0.0, 0.0, #12
                0.0, -0.125, 0.0,  0.0, 0.0, 0.0, #13
                0.5, -0.125, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.25, 0.0,  0.0, 0.0, 0.0
                ]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 0,
                4, 3, 5,
                5, 6, 4,
                7, 5, 8,
                8, 9, 5,
                9, 8, 10,
                10, 11, 9,
                10, 12, 13,
                12, 11, 13,
                7, 15, 8]

    return Shape(vertices, indices)

def createLetterA():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #0
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #1
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0, #2
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0, #3
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0, #4
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0, #5
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #6
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0, #7
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #8
                0.25, -0.5, 0.0, 0.0, 0.0, 0.0,#9
                -0.25, 0.0, 0.0,  0.0, 0.0, 0.0, #10
                0.25, 0.0, 0.0,  0.0, 0.0, 0.0, #11
                -0.25, -0.25, 0.0,  0.0, 0.0, 0.0, #12
                0.25, -0.25, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 5, 6,
                6, 0, 4,
                7, 1, 8,
                8, 7, 9,
                10, 11, 12,
                12, 13, 11]

    return Shape(vertices, indices)


def createLetterM():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, 0.25, 0.0, 0.0, 0.0, 0.0,
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.125, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.125, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.125, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.125, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.5, 0.0, 0.0, 0.0, 0.0
                ]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 0,
                4, 5, 6,
                6, 0, 4,
                7, 8, 9,
                9, 10, 8,
                11, 12, 13,
                13, 11, 3]

    return Shape(vertices, indices)


def createLetterO():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5 ,0.0,  0.0, 0.0, 0.0,
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, -0.5, 0.0, 0.0, 0.0, 0.0,
                -0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                0, 4, 6,
                6, 5, 0,
                5, 7, 9,
                9, 8, 7,
                10, 9, 11,
                11, 9, 1

                ]

    return Shape(vertices, indices)


def createLetterV():
    vertices = [
                -0.5, 0.5, 0.0,   0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                2, 4, 6,
                6, 5, 2

                ]

    return Shape(vertices, indices)

def createLetterR():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #0
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0, #1
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0, #2
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0, #3
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0, #4
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #5
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0, #6
                -0.5, -0.125, 0.0,  0.0, 0.0, 0.0, #7
                -0.5, 0.125, 0.0,  0.0, 0.0, 0.0, #8
                0.5, -0.125, 0.0,  0.0, 0.0, 0.0, #9
                0.5, 0.125, 0.0,  0.0, 0.0, 0.0, #10
                0.125, 0.5, 0.0,  0.0, 0.0, 0.0, #11
                0.125, -0.125, 0.0,  0.0, 0.0, 0.0, #12
                0.0, -0.125, 0.0,  0.0, 0.0, 0.0, #13
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0, #14
                0.25, -0.125, 0.0,  0.0, 0.0, 0.0, #15
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0] #16
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 0, 3,
                0, 4, 6,
                6, 0, 5,
                8, 10, 7,
                7, 9, 10,
                11, 1, 9,
                9, 11, 12,
                13, 16, 14,
                14, 15, 13]

    return Shape(vertices, indices)

def createLetterI():
    vertices = [
                0.0, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.0, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.25, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.125, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.125, 0.0,  0.0, 0.0, 0.0,
                0.0, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.25, -0.5, 0.0,  0.0, 0.0, 0.0 ]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 5, 6,
                6, 7, 5]
    return Shape(vertices, indices)


def createLetterC():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 5, 6,
                0, 4, 5,
                7, 5, 8,
                8, 5, 9]
    return Shape(vertices, indices)                 


def createLetterT():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.25, 0.0,  0.0, 0.0, 0.0,
                -0.125, 0.25, 0.0,  0.0, 0.0, 0.0,
                0.125, 0.25, 0.0,  0.0, 0.0, 0.0,
                -0.125, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.125, -0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 5, 6,
                6, 7, 5]
    return Shape(vertices, indices)

def createLetterY():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.0, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.15, 0.05, 0.0,  0.0, 0.0, 0.0,
                0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.125, -0.5, 0.0,  0.0, 0.0, 0.0,
                0.125, -0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 5, 6,
                6, 7, 5]
    return Shape(vertices, indices)


def createLetterL():
    vertices = [
                -0.5, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, 0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
                -0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.25, 0.0,  0.0, 0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 0.0, 0.0]
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
                0, 1, 2,
                2, 3, 1,
                4, 2, 6,
                6, 4, 5]
    return Shape(vertices, indices)

# shape de una linea
def createLine():
    vertices = [
                #Vertices         #Color
                 0.5,  0.5, 0.0,   0.36, 0.47, 0.53,
                -0.25, -0.45, 0.0,  0.36, 0.47, 0.53]
              
    indices = [0, 1]
    
    return Shape(vertices, indices)            

            


