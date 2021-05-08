"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


def crearGameOver(pipeline):
    gpuG = createGPUShape(bs.createLetterG(), pipeline)
    gpuA = createGPUShape(bs.createLetterA(), pipeline)
    gpuM = createGPUShape(bs.createLetterM(), pipeline)
    gpuO = createGPUShape(bs.createLetterO(), pipeline)
    gpuV = createGPUShape(bs.createLetterV(), pipeline)
    gpuR = createGPUShape(bs.createLetterR(), pipeline)

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

def crearVictory(pipeline):
    gpuV = createGPUShape(bs.createLetterV(), pipeline)
    gpuI = createGPUShape(bs.createLetterI(), pipeline)
    gpuC = createGPUShape(bs.createLetterC(), pipeline)
    gpuT = createGPUShape(bs.createLetterT(), pipeline)
    gpuO = createGPUShape(bs.createLetterO(), pipeline)
    gpuR = createGPUShape(bs.createLetterR(), pipeline)
    gpuY = createGPUShape(bs.createLetterY(), pipeline)
    gpuA = createGPUShape(bs.createLetterA(), pipeline)
    gpuL = createGPUShape(bs.createLetterL(), pipeline)
    gpuM = createGPUShape(bs.createLetterM(), pipeline)

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
    victoryNode.transform = tr.matmul([tr.translate(0.22, 0.2, 0.0),tr.scale(0.15,0.15,0)])
    victoryNode.childs = [vNode, iNode, cNode, tNode, oNode, rNode, yNode, rNode2, oNode2, yNode2, aNode, lNode, eNode]

    return victoryNode
# Crea el hospital
def crearEscenario(pipeline):

    # Las shapes utilizadas:
    gpuBlueGreenQuad = createGPUShape(bs.createColorQuad(0.411, 0.611, 0.592), pipeline)
    gpuDarkBlueGreenQuad = createGPUShape(bs.createColorQuad(0.266,0.44, 0.42 ), pipeline) 
    gpuGrayQuad = createGPUShape(bs.createColorQuad(0.537, 0.647, 0.714 ), pipeline)
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline)

    # Nodo de la muralla del hospital
    murallaNode = sg.SceneGraphNode("muralla")
    murallaNode.transform = tr.scale(2.0, 2.0, 1.0)
    murallaNode.childs = [gpuGrayQuad]

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

    # La salida
    salidaNode = sg.SceneGraphNode("salida")
    salidaNode.transform = tr.matmul([tr.translate(-0.9,0.8,0), tr.scale(0.3,0.4,1.0)])
    salidaNode.childs = [gpuWhiteQuad]  

    # Nodo que junta todo lo del escenario
    escenarioNode = sg.SceneGraphNode("escenario")
    escenarioNode.childs = [murallaNode, sueloNode, sueloOscuroNode, disenoCuadradoNode, salidaNode]


    return escenarioNode

def crearSalida(pipeline):
    gpuGrayQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline)
    return salidaNode

