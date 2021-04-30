""" P3 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
import random as rand
from shapes import *
from model import *


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False
        self.x = 0
        self.garbageX = 0


# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 800
    height = 800
    title = "P3 - Drive simulator"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    

    # Grafo de escena del background
    "mainScene = createScene(pipeline)"
    # Se añade el auto a la escena principal
    "mainScene.childs += [car]"

    
    # Shape con textura del jugador
    playerModel = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/tu.png")

    # Shape con textura de la carga
    garbage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/zombie-0.png")

   

    # Se crea el nodo del player
    playerNode = sg.SceneGraphNode("player")
    playerNode.childs = [playerModel]

    # Se crean dos nodos de carga
    garbageNode = sg.SceneGraphNode("garbage")
    garbageNode.childs = [garbage]

    # Se crea una agrupacion de basura
    garbageGroup = sg.SceneGraphNode("gGroup")
    garbageGroup.childs = []

    # Se crean el grafo de escena con textura y se agregan las cargasb
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [playerNode,garbageGroup]

    #Player
    player = Player(0.1)
    player.set_model(playerNode)
    player.set_controller(controller)


    # Lista con todas las cargas
    cargas = []

    # Crear una basura
    def instatiateGarbage(x,y,tag):
        global cargas 
        newGarbage = sg.SceneGraphNode(tag)
        newGarbage.childs = [garbageNode]

        garbageGroup.childs += [newGarbage]
        carga = Carga(x,y,0.1)
        carga.set_model(newGarbage)
        carga.update()

        cargas += [carga]
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    t_inicial = 0
    t_pasado = 0
    cooldown = 0.8

    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        controller.x -= 0.5*delta
        if (controller.x <= -2):
            controller.x = 0

        #Control de spawn de basura
        t_pasado = t1 - t_inicial

        """if( t_pasado >= cooldown):
            instatiateGarbage(1.1,rand.uniform(-0.85,-0.45),"garbage")
            t_inicial = t1"""

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Se llama al metodo del player para detectar colisiones
        player.collision(cargas)
        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)
        print(player.pos)

        # Se crea el movimiento de giro del rotor
        #rotor = sg.findNode(mainScene, "rtRotor")
        #rotor.transform = tr.rotationZ(t1)

        #Movimiento de la basura
        for carga in cargas:
            carga.pos[0]-=1*delta
            carga.update()

            #Aqui se deberia comprobar para eliminar
            #si esta muy lejos pero no estoy seguro como


        # Se dibuja el grafo de escena principal
        "glUseProgram(pipeline.shaderProgram)"
        #g.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    "mainScene.clear()"
    tex_scene.clear()
    
    glfw.terminate()