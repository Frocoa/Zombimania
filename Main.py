""" P3 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from grafica.gpu_shape import GPUShape
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

# Shader
class SimpleTextureTransformShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 130

            uniform mat4 transform;
            uniform float index;

            in vec3 position;
            in vec2 texCoords;

            out vec2 outTexCoords;

            void main()
            {
                vec2 newTexCoord;
                gl_Position = transform * vec4(position, 1.0f);
                newTexCoord = vec2(texCoords.x/2*index,texCoords.y);
                outTexCoords = newTexCoord;
            }
            """

        fragment_shader = """
            #version 130

            in vec2 outTexCoords;

            out vec4 outColor;

            uniform sampler2D samplerTex;

            void main()
            {
                outColor = texture(samplerTex, outTexCoords);
            }
            """

        # Compiling our shader program
        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + 2d texture coordinates => 3*4 + 2*4 = 20 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        texCoords = glGetAttribLocation(self.shaderProgram, "texCoords")
        glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(3 * SIZE_IN_BYTES))
        glEnableVertexAttribArray(texCoords)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        glBindVertexArray(gpuShape.vao)
        glBindTexture(GL_TEXTURE_2D, gpuShape.texture)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

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
    title = "Zombimania"
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

    tex_pipeline = SimpleTextureTransformShaderProgram()

    #tex2_pipeline = SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.051, 0.09, 0.109, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    

    # Grafo de escena del background
    mainScene = crearEscenario(pipeline)
    # Se añade el auto a la escena principal
    "mainScene.childs += [car]"

    

    # Shape con textura del jugador
    playerModelList = []
    for i in range(6):
    	model = createTextureGPUShape(bs.createMultiTextureQuad(i/6,(i+1)/6,0,1), tex_pipeline, "sprites/playerSheet.png")
    	playerModelList += [model]

    # Shape con textura de la zombie
    zombieModelList = []
    for i in range(7):
        model = createTextureGPUShape(bs.createMultiTextureQuad(i/7,(i+1)/7,0,1), tex_pipeline, "sprites/zombieSheet.png")
        zombieModelList += [model]

   

    # Se crea el nodo del player
    playerNode = sg.SceneGraphNode("player")
    playerNode.childs = [playerModelList[0]]

    # Se crean dos nodos de zombie
    zombieNode = sg.SceneGraphNode("zombie")
    zombieNode.childs = [zombieModelList[0]]

    # Se crea una agrupacion de zombies
    zombieGroup = sg.SceneGraphNode("zGroup")
    zombieGroup.childs = []

    # Se crean el grafo de escena con textura y se agregan los zombies
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [playerNode,zombieGroup]

    #Player
    player = Player(0.08)
    player.set_model(playerNode)
    player.set_controller(controller)


    # Lista con todas los zombies
    zombieList = []

    # Crear una basura
    def instantiateZombie(x,y,tag):
        global zombieList 
        newZombie = sg.SceneGraphNode(tag)
        newZombie.childs = [zombieNode]

        speed = rand.uniform(0.1,0.5)
        zombieGroup.childs += [newZombie]
        goingUpwards = bool(rand.getrandbits(1))
        zombie = Zombie(x,y,0.12,speed,goingUpwards)
        zombie.set_model(newZombie)
        zombie.update()

        zombieList += [zombie]
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    t_inicial = 0
    t_pasado = 0
    zombieCooldown = 0.1

    i = 0
    z = 0
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        controller.x -= 0.5*delta
        if (controller.x <= -2):
            controller.x = 0

        #Control de spawn de zombies
        t_pasado = t1 - t_inicial

        if( t_pasado >= zombieCooldown):
            instantiateZombie(rand.uniform(-0.7,0.7), 1.1, "garbage")
            playerNode.childs = [playerModelList[i]]
            zombieNode.childs = [zombieModelList[z]]
            i = (i+1)%6
            z = (z+1)%7
            t_inicial = t1

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
        player.collision(zombieList)
        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)



        #Movimiento de los zombies
        for zombie in zombieList:
            if (zombie.goingUpwards):
                zombie.pos[1]+=zombie.speed*delta

            else:
                zombie.pos[1]-=zombie.speed*delta

            zombie.update()

            #Aqui se deberia comprobar para eliminar
            #si esta muy lejos pero no estoy seguro como


        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()