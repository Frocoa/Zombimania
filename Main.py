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

    # Shape con textura del jugador
    playerModelList = []
    for i in range(6):
    	model = createTextureGPUShape(bs.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/playerSheet.png")
    	playerModelList += [model]

    # Shape con textura del jugador cuando este muriendo
    playerDyingModelList = []
    for i in range(6):
        model = createTextureGPUShape(bs.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/playerDyingSheet.png")
        playerDyingModelList += [model]

    # Shape con textura de la zombie
    zombieModelList = []
    for i in range(7):
        model = createTextureGPUShape(bs.createMultiTextureQuad(i/7, (i+1)/7, 0, 1), tex_pipeline, "sprites/zombieSheet.png")
        zombieModelList += [model]

    # Shape con textura de los humanosw
    humanModelList = []
    for i in range(6):
        model = createTextureGPUShape(bs.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/humanSheet.png")
        humanModelList += [model]
   

    # Se crea el nodo del player
    playerNode = sg.SceneGraphNode("player")
    playerNode.childs = [playerModelList[0]]

    # Se crean un nodo de zombi
    #zombieNode = sg.SceneGraphNode("zombie")
    #zombieNode.childs = [zombieModelList[0]]

    # Se crea una agrupacion de zombies
    zombieGroup = sg.SceneGraphNode("zGroup")
    zombieGroup.childs = []

    # Se crea un nodo de humano
    humanNode = sg.SceneGraphNode("human")
    humanNode.childs = [humanModelList[0]]

    # Se crea una agrupacion de humanos
    humanGroup = sg.SceneGraphNode("hGroup")
    humanGroup.childs = []

    # Se crean el grafo de escena con textura y se agregan los zombies
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [playerNode,zombieGroup, humanGroup]

    #Player
    player = Player(0.08, 0.16)
    player.set_model(playerNode)
    player.set_controller(controller)


    # Lista con todas los zombies
    zombieList = []
    humanList = []

    # Crear un zombie
    def instantiateZombie(x,y):
        global zombieList 
        newZombie = sg.SceneGraphNode("zombie")
        newZombie.childs = [zombieModelList[0]]

        speed = rand.uniform(0.2, 0.3)
        zombieGroup.childs += [newZombie]
        goingUpwards = bool(rand.getrandbits(1))
        zombie = Zombie(x, y, 0.12, speed, goingUpwards)
        zombie.set_model(newZombie)
        zombie.update()

        zombieList += [zombie]

    def instantiateHuman(x,y,tag):
        global humanList 
        newHuman = sg.SceneGraphNode(tag)
        newHuman.childs = [humanNode]

        speed = rand.uniform(0.1, 0.5)
        humanGroup.childs += [newHuman]
        goingUpwards = bool(rand.getrandbits(1))
        human = Human(x, y, 0.08, speed, goingUpwards, True)
        human.set_model(newHuman)
        human.update()

        humanList += [human]   


    def changePlayerFrame(frameIndex):
        # Se pasa al siguiente frame del jugador
        if player.deathRolls <= 4:
            playerNode.childs = [playerModelList[frameIndex]]

        else:
            playerNode.childs = [playerDyingModelList[frameIndex]] 
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    t_inicial = 0
    

    z = 0
    tamañoHorda = 5
    tamañoGrupoHumanos = 1
    zombieCooldown = 2.0

    playerAnimPeriod = 0.08
    playerAnimMoment = 0
    while not glfw.window_should_close(window):

        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        
        # Control de la animacion del jugador
        sinceLastFrame = t1 - playerAnimMoment
  
        if (player.isAlive == False):
            playerNode.childs = [zombieModelList[0]]
            (player.sizeX, player.sizeY) = (0.115, 0.161)  

        # Control de spawn de zombies y humanos
        t_pasado = t1 - t_inicial

        if( t_pasado >= zombieCooldown):

            for n in range(tamañoHorda):
                instantiateZombie(rand.uniform(-0.7,0.7), 1.1)
                
            
            """for n in range(tamañoGrupoHumanos):
                instantiateHuman(rand.uniform(-0.7, 0.7), 1.1, "human")"""

            z = (z+1)%7
            t_inicial = t1

        for zombie in zombieList:
                zombie.model.childs = [zombieModelList[zombie.spriteIndex]]

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # El personaje tiene animacion solo al moverse
        if (controller.is_a_pressed or controller.is_d_pressed or controller.is_s_pressed or controller.is_w_pressed):
            if (player.isAlive):
                changePlayerFrame(player.nextSpriteIndex())

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

        # Movimiento de los zombies
        for zombie in zombieList:
            zombie.pos[1] -= zombie.speed * delta
            zombie.update()


        # Movimiento de los humanos
        for human in humanList:
            if (human.goingUpwards):
                human.pos[1] += human.speed * delta
            
            else:
                human.pos[1] -= human.speed * delta

            human.update()


        #Borrar zombies
        for zombie in zombieList:
            if zombie.shouldBeRemoved:
                zombie.remove(zombieGroup, zombieList)

        #Debug de rendimiento
        """print("###########################################")
        print("Cantidad de objeto zombie:", len(zombieList))
        print("Cantidad de zombies en ZombieGroup:", len(zombieGroup.childs))
        print("Se lleva corriendo:",t1,"segundos")
        print("###########################################")"""

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