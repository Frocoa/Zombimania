"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.shaders as shad
import grafica.shapes as shapes
import grafica.transformations as tr
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = shad.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = shad.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = shad.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

# Se crea la shape de la puerta de salida
def crearSalida(tex_pipeline):
    model = createTextureGPUShape(shapes.createTextureQuad(1,1), tex_pipeline, "sprites/salida.png")
    salidaNode = sg.SceneGraphNode("salida")
    salidaNode.transform = tr.matmul([tr.translate(-0.74,0.8,0), tr.scale(0.3,0.4,1.0)])
    salidaNode.childs = [model]
    return salidaNode

#Se crea la shape con textura de la decoraciones que hay en el hospital
def crearDecoracion(tex_pipeline):
    shapeDecoraction = shapes.createTextureQuad(1,2)
    gpuDecoration = shad.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuDecoration)
    gpuDecoration.fillBuffers(shapeDecoraction.vertices, shapeDecoraction.indices, GL_STATIC_DRAW)
    gpuDecoration.texture = shad.textureSimpleSetup(
        "sprites/decoracion.png", GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    decoracionNode = sg.SceneGraphNode("decoracion")
    decoracionNode.transform = tr.scale(2.0,2.9,0)
    decoracionNode.childs = [gpuDecoration]
    return decoracionNode

# Se crea el grafo con la palabra "Game Over"
def crearGameOver(pipeline):
    #Los shapes de cada letra
    gpuG = createGPUShape(shapes.createLetterG(), pipeline)
    gpuA = createGPUShape(shapes.createLetterA(), pipeline)
    gpuM = createGPUShape(shapes.createLetterM(), pipeline)
    gpuO = createGPUShape(shapes.createLetterO(), pipeline)
    gpuV = createGPUShape(shapes.createLetterV(), pipeline)
    gpuR = createGPUShape(shapes.createLetterR(), pipeline)

    # Se crea el nodo con la G
    gNode = sg.SceneGraphNode("G")
    gNode.transform = tr.translate(-5.1,0,0)
    gNode.childs = [gpuG]
    # Se crea el nodo con la A
    aNode = sg.SceneGraphNode("A")
    aNode.transform = tr.translate(-4,0,0)
    aNode.childs = [gpuA]
    # Se crea el nodo con la M
    mNode = sg.SceneGraphNode("M")
    mNode.transform = tr.translate(-2.9,0,0)
    mNode.childs = [gpuM]
    # Se crea el nodo con la E
    eNode = sg.SceneGraphNode("E")
    eNode.transform = tr.matmul([tr.translate(-1.8,0,0),tr.rotationZ(1.5708)])
    eNode.childs = [gpuM]
    # Se crea el nodo con la O
    oNode = sg.SceneGraphNode("O")
    oNode.transform = tr.translate(0.4,0,0)
    oNode.childs = [gpuO]
    # Se crea el nodo con la V
    vNode = sg.SceneGraphNode("V")
    vNode.transform = tr.translate(1.5,0,0)
    vNode.childs = [gpuV]
    # Se crea el nodo con la E2
    eNode2 = sg.SceneGraphNode("E2")
    eNode2.transform = tr.matmul([tr.translate(2.6,0,0),tr.rotationZ(1.5708)])
    eNode2.childs = [gpuM] 
    # Se crea el nodo con la G
    rNode = sg.SceneGraphNode("R")
    rNode.transform = tr.translate(3.7,0,0)
    rNode.childs = [gpuR]

    # Se crea el nodo del Game Over
    gameOverNode = sg.SceneGraphNode("GameOver")
    gameOverNode.transform = tr.matmul([tr.translate(0.1, 0.0, 0.0),tr.scale(0.15,0.15,0)])
    gameOverNode.childs = [gNode, aNode, mNode, eNode, oNode, vNode, eNode2, rNode]

    return gameOverNode

# Se crea el grafo con la frase "Victory Royale"
def crearVictory(pipeline):
    #Los shapes de cada letra
    gpuV = createGPUShape(shapes.createLetterV(), pipeline)
    gpuI = createGPUShape(shapes.createLetterI(), pipeline)
    gpuC = createGPUShape(shapes.createLetterC(), pipeline)
    gpuT = createGPUShape(shapes.createLetterT(), pipeline)
    gpuO = createGPUShape(shapes.createLetterO(), pipeline)
    gpuR = createGPUShape(shapes.createLetterR(), pipeline)
    gpuY = createGPUShape(shapes.createLetterY(), pipeline)
    gpuA = createGPUShape(shapes.createLetterA(), pipeline)
    gpuL = createGPUShape(shapes.createLetterL(), pipeline)
    gpuM = createGPUShape(shapes.createLetterM(), pipeline)

    # Se crea el nodo con la V
    vNode = sg.SceneGraphNode("V")
    vNode.transform = tr.translate(-4.5,0,0)
    vNode.childs = [gpuV]
    # Se crea el nodo con la I
    iNode = sg.SceneGraphNode("I")
    iNode.transform = tr.translate(-3.8,0,0)
    iNode.childs = [gpuI]
    # Se crea el nodo con la C
    cNode = sg.SceneGraphNode("C")
    cNode.transform = tr.translate(-2.9,0,0)
    cNode.childs = [gpuC]
    # Se crea el nodo con la T
    tNode = sg.SceneGraphNode("T")
    tNode.transform = tr.translate(-1.8,0,0),tr.rotationZ(1.5708)
    tNode.childs = [gpuT]
    # Se crea el nodo con la O
    oNode = sg.SceneGraphNode("O")
    oNode.transform = tr.translate(-0.7,0,0)
    oNode.childs = [gpuO]
    # Se crea el nodo con la R
    rNode = sg.SceneGraphNode("R")
    rNode.transform = tr.translate(0.4,0,0)
    rNode.childs = [gpuR]
    # Se crea el nodo con la Y
    yNode = sg.SceneGraphNode("Y")
    yNode.transform = tr.translate(1.5,0,0),tr.rotationZ(1.5708)
    yNode.childs = [gpuY] 

    # Se crea el nodo con la R2
    rNode2 = sg.SceneGraphNode("R2")
    rNode2.transform = tr.translate(-4.2,-1.2,0)
    rNode2.childs = [gpuR]
    # Se crea el nodo con la O2
    oNode2 = sg.SceneGraphNode("O2")
    oNode2.transform = tr.translate(-3.1,-1.2,0)
    oNode2.childs = [gpuO]
    # Se crea el nodo con la Y
    yNode2 = sg.SceneGraphNode("Y")
    yNode2.transform = tr.translate(-2.0,-1.2,0)
    yNode2.childs = [gpuY] 
    # Se crea el nodo con la A
    aNode = sg.SceneGraphNode("A")
    aNode.transform = tr.translate(-0.9,-1.2,0)
    aNode.childs = [gpuA]
    # Se crea el nodo con la L
    lNode = sg.SceneGraphNode("L")
    lNode.transform = tr.translate(0.2,-1.2,0)
    lNode.childs = [gpuL]
    # Se crea el nodo con la E
    eNode = sg.SceneGraphNode("E")
    eNode.transform = tr.matmul([tr.translate(1.3,-1.2,0),tr.rotationZ(1.5708)])
    eNode.childs = [gpuM]

    # Se crea el nodo del Game Over
    victoryNode = sg.SceneGraphNode("Victory")
    victoryNode.transform = tr.matmul([tr.translate(0.22, 0., 0.0),tr.scale(0.15,0.15,0)])
    victoryNode.childs = [vNode, iNode, cNode, tNode, oNode, rNode, yNode, rNode2, oNode2, yNode2, aNode, lNode, eNode]

    return victoryNode

# Crea el hospital
def createGeometricScene(pipeline):

    # Las shapes utilizadas:
    gpuBlueGreenQuad = createGPUShape(shapes.createColorQuad(0.411, 0.611, 0.592), pipeline)
    gpuDarkBlueGreenQuad = createGPUShape(shapes.createColorQuad(0.266,0.44, 0.42 ), pipeline) 
    gpuGrayQuad = createGPUShape(shapes.createColorQuad(0.537, 0.647, 0.714 ), pipeline)
    gpuLine = createGPUShape(shapes.createLine(), pipeline)

    # Nodo del muro del hospital
    muroNode = sg.SceneGraphNode("muro")
    muroNode.transform = tr.scale(2.0, 2.0, 1.0)
    muroNode.childs = [gpuGrayQuad]

    # Nodo de la muralla (Muro + diseño de lienas)
    murallaNode = sg.SceneGraphNode("muralla")
    murallaNode.childs = [muroNode]

    # Nodo del suelo del hostpial que es un quad azul
    sueloNode = sg.SceneGraphNode("suelo")
    sueloNode.transform = tr.scale(1.5,2.0,1.0)
    sueloNode.childs = [gpuBlueGreenQuad]

    # Nodo de la parte oscura del suelo
    sueloOscuroNode = sg.SceneGraphNode("sueloOscuro")
    sueloOscuroNode.transform = tr.scale(1.0,2.0,1.0)
    sueloOscuroNode.childs = [gpuDarkBlueGreenQuad]

    # Nodo del cuadrado claro
    cuadradoClaroNode = sg.SceneGraphNode("cuadClaro")
    cuadradoClaroNode.transform = tr.scale(0.666, 0.666, 1.0)
    cuadradoClaroNode.childs = [gpuBlueGreenQuad]

    # Nodo del cuadrado oscuro
    cuadradoOscuroNode = sg.SceneGraphNode("cuadOscuro")
    cuadradoOscuroNode.transform = tr.scale(0.333, 0.333, 1.0)
    cuadradoOscuroNode.childs = [gpuDarkBlueGreenQuad]

    # Nodo con el diseño de cuadrados
    disenoCuadradoNode = sg.SceneGraphNode("diseno")
    disenoCuadradoNode.transform = tr.translate(0.0, 0.6, 0.0 )  
    disenoCuadradoNode.childs = [cuadradoClaroNode, cuadradoOscuroNode]

    # Nodo con el diseño de cuadrados2
    disenoCuadradoNode2 = sg.SceneGraphNode("diseno2")
    disenoCuadradoNode2.transform = tr.translate(0.0, -0.8, 0.0 )  
    disenoCuadradoNode2.childs = [cuadradoClaroNode, cuadradoOscuroNode]

    # Nodo que tiene todo el piso
    pisoNode = sg.SceneGraphNode("piso")
    pisoNode.childs = [sueloNode, sueloOscuroNode, disenoCuadradoNode, disenoCuadradoNode2]

    # Nodo que junta todo lo del escenario
    escenarioNode = sg.SceneGraphNode("escenario")
    escenarioNode.childs = [murallaNode, pisoNode]

    # Nodo de las lineas de la muralla
    for i in range(9):
        lineaNode = sg.SceneGraphNode("linea")
        lineaNode.transform = tr.matmul([tr.translate(-0.90, -1 + 2/8 * i, 0.0), tr.scale(0.3,0.2,1.0)])
        lineaNode.childs = [gpuLine]
        murallaNode.childs += [lineaNode]

        lineaNode2 = sg.SceneGraphNode("linea")
        lineaNode2.transform = tr.matmul([tr.translate(0.90, -1 + 2/8*i, 0.0), tr.scale(0.3, 0.2, 1.0), tr.rotationZ(1.5708)])
        lineaNode2.childs = [gpuLine]
        murallaNode.childs += [lineaNode2]

    return escenarioNode

