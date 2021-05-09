
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

import math

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]


def applyOffset(shape, stride, offset):

    numberOfVertices = len(shape.vertices)//stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):

    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]


def createAxis(length=1.0):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        -length,  0.0,  0.0, 0.0, 0.0, 0.0,
         length,  0.0,  0.0, 1.0, 0.0, 0.0,

         0.0, -length,  0.0, 0.0, 0.0, 0.0,
         0.0,  length,  0.0, 0.0, 1.0, 0.0,

         0.0,  0.0, -length, 0.0, 0.0, 0.0,
         0.0,  0.0,  length, 0.0, 0.0, 1.0]

    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
         0, 1,
         2, 3,
         4, 5]

    return Shape(vertices, indices)


def createRainbowTriangle():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowCircle(N):

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
             math.cos(theta*3.14*i/360)*math.cos(theta*2*3.14*i/360),  math.cos(theta*3.14*i/360)*math.sin(theta*2*3.14*i/360), 0,

            # color generates varying between 0 and 1
                  math.sin(theta),       math.cos(theta), 0]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]


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
            #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
                14, 15, 13
                ]

    return Shape(vertices, indices)

def createLetterI():
    vertices = [
    #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
    #   positions        colors
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
