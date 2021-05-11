""" P3 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.shapes 
import grafica.shaders as shad
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from grafica.gpu_shape import GPUShape
import random as rand
from nodos import *
from clases import *
import sys

z = int(sys.argv[1])
h = int(sys.argv[2])
t = float(sys.argv[3])
p = float(sys.argv[4])


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False
        self.is_e_pressed = False
        self.is_q_pressed = False
        self.gameWon = False
        self.useGoogles = False

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

    # Caso de detectar la tecla [E], actualiza estado de variable
    if key == glfw.KEY_E:
        if action ==glfw.PRESS:
            controller.is_e_pressed = True
        elif action == glfw.RELEASE:
            controller.is_e_pressed = False

    # Caso de detectar la tecla [Q], actualiza estado de variable
    if key == glfw.KEY_Q:
        if action ==glfw.PRESS:
            controller.is_q_pressed = True
        elif action == glfw.RELEASE:
            controller.is_q_pressed = False                   

    # Caso de detecar la barra espaciadora, se activa el visor de infección
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.useGoogles = not controller.useGoogles

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
    pipeline = shad.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas de un solo color transparente
    transparentTexPipeline = shad.TransparentTextureShaderProgram()
    # Pipeline estandar para dibujar shapes con texturas
    tex_pipeline = shad.SimpleTextureTransformShaderProgram() 
    # Pipeline para las transiciones de colores
    colorPipeline = shad.ScreenEffectShaderProgram()
    # Pipeline para el efecto de alucinacion cuando estas infectado
    infectedPipeline = shad.InfectedTransformShaderProgram()
    # Setting up the clear screen color
    glClearColor(0.051, 0.09, 0.109, 1.0)

    # Activando transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    # Grafo de escena del background
    mainScene = createGeometricScene(pipeline)

    # Shapes con la textura del jugador
    playerModelList = []
    for i in range(6):
    	model = createTextureGPUShape(shapes.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/playerSheet.png")
    	playerModelList += [model]

    # Shapes con textura del jugador cuando esta cansado
    playerBreathingModel = []
    for i in range(6):
        model = createTextureGPUShape(shapes.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/playerDyingSheet.png")
        playerBreathingModel += [model]

    # Shapes con la textura de un zombi
    zombieModelList = []
    for i in range(7):
        model = createTextureGPUShape(shapes.createMultiTextureQuad(i/7, (i+1)/7, 0, 1), tex_pipeline, "sprites/zombieSheet.png")
        zombieModelList += [model]

    # Shapes con textura de un humano
    humanModelList = []
    for i in range(6):
        model = createTextureGPUShape(shapes.createMultiTextureQuad(i/6, (i+1)/6, 0, 1), tex_pipeline, "sprites/humanSheet.png")
        humanModelList += [model]
   
    # Shape con la textura de la calavera
    skullModel = createTextureGPUShape(shapes.createTextureSkull(), tex_pipeline, "sprites/skull.png")

    # Shape de las alas doradas
    wingsModel = createGPUShape(shapes.createWings(14), pipeline)

    #Nodo de la calavera
    skullNode = sg.SceneGraphNode("skull")
    skullNode.childs = [skullModel]

    #Nodo de las alas de victoria
    wingsNode = sg.SceneGraphNode("wings")
    wingsNode.transform = tr.matmul([tr.translate(0.0, -0.2, 0.0), tr.scale(1.1, 1.1, 1.0)])
    wingsNode.childs = [wingsModel]

    # Se crea la shape de la pantalla roja
    pantallaRoja = createGPUShape(shapes.createColorQuad(0.35,0.0,0.0), colorPipeline)
    # Se crea la shape de victoria
    victory = crearVictory(colorPipeline)
    # Se crea la shape de game over
    gameOver = crearGameOver(colorPipeline)

    # Nodo de la pantalla
    pantallaNode = sg.SceneGraphNode("pantalla")
    pantallaNode.transform = tr.scale(2,2,1)
    pantallaNode.childs = [pantallaRoja]

    # Nodo de victory royale
    victoryNode = sg.SceneGraphNode("victory")
    victoryNode.transform = tr.translate(2.0,0,0) # Para evitar que salga un frame en el centro antes de tiempo
    victoryNode.childs = [victory]

    # Nodo de la pantalla de victoria junto a los efectos
    victoryScreenNode = sg.SceneGraphNode("victoryScreen")
    victoryScreenNode.childs = []

    # Nodo de game over
    gameOverNode = sg.SceneGraphNode("gameOver")
    gameOverNode.transform = tr.translate(2.0, 0.0, 0.0)  # Para evitar que salga un frame en el centro antes de tiempo
    gameOverNode.childs = [gameOver]

    # Escena de la interfaz
    hudScene = sg.SceneGraphNode("hud")
    hudScene.childs = [pantallaNode]

    # Se crea el nodo del player
    playerNode = sg.SceneGraphNode("player")
    playerNode.childs = [playerModelList[0]]

    # Se crea un nodo de todos los zombies
    zombieGroup = sg.SceneGraphNode("zGroup")
    zombieGroup.childs = []

    # Se crea una agrupacion de humanos
    humanGroup = sg.SceneGraphNode("hGroup")
    humanGroup.childs = []

    # Se crean el grafo de escena con textura y se agregan los zombies
    texScene = sg.SceneGraphNode("textureScene")
    texScene.childs = [crearDecoracion(tex_pipeline),crearSalida(tex_pipeline),playerNode,
                        zombieGroup, humanGroup]

    

    # Instanciar al jugador
    player = Player(0.08, 0.16)
    player.set_model(playerNode)
    player.set_controller(controller)


    # Lista con todos los objetos
    zombieList = []
    humanList = []
    infectedList = []
    starList = []

    # Estrella movil
    glUseProgram(pipeline.shaderProgram)
    starVertices = shapes.movileStarVertices(0)
    starShape = shapes.createMovileStar(starVertices)
    gpuStarShape = shad.GPUShape().initBuffers()
    pipeline.setupVAO(gpuStarShape)
    gpuStarShape.fillBuffers(starShape.vertices, starShape.indices, GL_STREAM_DRAW)
  
    starNode = sg.SceneGraphNode("starGroup")
    starNode.childs = []
    

    # Crear una instancia de zombi
    def instantiateZombie(x,y,goingUpwards):
        global zombieList
        newZombie = sg.SceneGraphNode("zombie")
        newZombie.childs = [zombieModelList[0]]

        speed = rand.uniform(0.2, 0.3)
        zombieGroup.childs += [newZombie]
        zombie = Zombie(x, y, 0.12, speed, goingUpwards)
        zombie.set_model(newZombie)
        zombie.update()

        zombieList += [zombie]

    # Crear una instancia de humano
    def instantiateHuman(x, y, goingUpwards):
        global humanList
        newHuman = sg.SceneGraphNode("human")
        newHuman.childs = [humanModelList[0]]

        speed = rand.uniform(0.2, 0.5)
        humanGroup.childs += [newHuman]
        isInfected = bool(rand.getrandbits(1))
        human = Human(x, y, 0.08, speed, goingUpwards, isInfected)
        human.set_model(newHuman)
        human.update()

        humanList += [human]

    # Crear una instancia de estrella
    def instantiateStar(x,y):
        global starList
        newStar = sg.SceneGraphNode("star")
        newStar.transform = tr.translate(x,y,0)
        newStar.childs = [gpuStarShape]
        starNode.childs += [newStar]

        star = Star(x,y)
        star.setModel(newStar)
        starList += [star]

    # Manejo de la animacion del jugador
    def changePlayerFrame(frameIndex):
        # Se pasa al siguiente frame del jugador

        # Jugador en estado normal
        if player.dashTimePassed >= player.dashCooldown:
            playerNode.childs = [playerModelList[frameIndex]]

        # Jugador recueprando el aliento
        else:
            playerNode.childs = [playerBreathingModel[frameIndex]] 


    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()


    t_inicial = 0
    
    # parametros de la animacion del jugador
    playerAnimPeriod = 0.08
    playerAnimMoment = 0

    # parametros de las animaciones
    transparency = 10.0
    victoryPos = 10.0
    shearingEffect = 15.0
    infectedFloat = 0.0

    # estado de la partida
    alreadyDead = False # perder
    alreadyWon = False # ganar

    # grosor de las lineas de la muralla
    glLineWidth(3)


    # update del juego
    while not glfw.window_should_close(window):

        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        
        # Control de la animacion del jugador
        sinceLastFrame = t1 - playerAnimMoment
        t_pasado = t1 - t_inicial

        # El personaje tiene animacion solo al moverse
        if (controller.is_a_pressed or controller.is_d_pressed or \
            controller.is_s_pressed or  controller.is_w_pressed):
            if (player.isAlive and not controller.gameWon):
                changePlayerFrame(player.nextSpriteIndex())

        # Control de animacion de zombis
        for zombie in zombieList:
                zombie.model.childs = [zombieModelList[zombie.spriteIndex]]
        # Control de animacion de humanos
        for human in humanList:
                human.model.childs = [humanModelList[human.spriteIndex]]
        
        # Todo lo que ocurre cada T segundos
        if( t_pasado >= t):

            # se instancian z zombis
            for n in range(z):
                instantiateZombie(rand.uniform(-0.7,0.7), 1.1, bool(rand.getrandbits(1)))
            # se instancian h humanos
            for n in range(h):
                instantiateHuman(rand.uniform(-0.7, 0.7), 1.1, bool(rand.getrandbits(1)))
            # se revisa si un humano se vuelve zombi
            for human in humanList:
                if human.isInfected:
                    human.deathRoll(p)
            # Se revisa si el jugador se vuelve zombi
            if player.isInfected:
                player.deathRoll(p)

            t_inicial = t1

        # Manejo de los vertices de las estrellas
        if(controller.gameWon):
            starVertices = shapes.movileStarVertices(t1)
            vertexData = np.array(starVertices, dtype=np.float32)
            glBindBuffer(GL_ARRAY_BUFFER, gpuStarShape.vbo)
            # Se usa un estilo de dibujo dinamico
            glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, GL_STREAM_DRAW)

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Se llama al metodo del player para detectar colisiones
        if(player.isAlive and not player.dashing and not controller.gameWon):
         player.collision(zombieList, humanList)
         player.checkWin()
        # Se llama al metodo del jugador para actualizar su estado
        player.update(delta)

        # Ocurre una vez al perder la partida
        if player.isAlive == False and alreadyDead == False:
            playerNode.childs = []
            hudScene.childs += [gameOverNode]
            skullNode.transform = tr.matmul([tr.translate(player.pos[0], \
                                             player.pos[1], 0), tr.scale(0.15, 0.15, 1.0)])
            texScene.childs += [skullNode]
            instantiateZombie(player.pos[0], player.pos[1], False)

            alreadyDead = True

        # Ocurre una vez al ganar la partida
        if(controller.gameWon == True and alreadyWon == False):
            hudScene.childs += [victoryNode]
            victoryScreenNode.childs += [starNode, wingsNode, victoryNode]
            playerNode.childs = []

            # Se generan 13 estrellas
            for n in range(13):
                instantiateStar(0.8*math.cos(n/2),0.8*math.sin(n/2))
            for star in starList:
             star.getModel().transform = tr.matmul([tr.translate(star.getPosX(), star.getPosY(), 0.0) \
                                                    ,tr.scale(0.1,0.1,1.0),tr.rotationZ(t1*2)])
            alreadyWon = True

        # Maenjo de los zombies
        for zombie in zombieList:
            zombie.pos[1] -= zombie.speed * delta

            if zombie.goingRight == True:
                zombie.pos[0] += zombie.speed * delta * 0.8
            else:
                zombie.pos[0] -= zombie.speed * delta * 0.8

            zombie.collision(humanList)
            zombie.update()

        # Manejo de los humanos
        for human in humanList:
            human.pos[1] -= human.speed * delta

            if human.goingRight == True:
                human.pos[0] += human.speed * delta * 0.8
            else:
                human.pos[0] -= human.speed * delta * 0.8    

            human.collision(zombieList, humanList)
            human.update()

            if human.isAlive == False:
                instantiateZombie(human.pos[0], human.pos[1], False)
                human.remove(humanGroup, humanList)

            if human.isInfected == True:
                infectedList += [human]    


        #Borrar zombies fuera del mapa
        for zombie in zombieList:
            if zombie.shouldBeRemoved:
                zombie.remove(zombieGroup, zombieList)

        #Borrar los humanos fuera del mapa
        for human in humanList:
            if human.shouldBeRemoved:
                human.remove(humanGroup, humanList)

        
        # Se dibuja el grafo de escena principal
        if player.isInfected and player.isAlive and not controller.gameWon:
            glUseProgram(infectedPipeline.shaderProgram)
            sg.drawSceneGraphInfected(mainScene,infectedPipeline,"transform", infectedFloat)
            infectedFloat += 0.01
        else:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNodeTex(texScene, tex_pipeline, "transform", False )

        if controller.useGoogles == True:
            glUseProgram(transparentTexPipeline.shaderProgram)
            googleTransparency = shapes.clamp(math.cos(t1*5), 0.4, 0.8)
            for human in humanList:
                if human in infectedList:
                    sg.drawSceneGraphNodeTex(human.model, transparentTexPipeline, "transform", True, googleTransparency)
            if player.isInfected == True:
                sg.drawSceneGraphNodeTex(player.model, transparentTexPipeline, "transform", True, googleTransparency)

        # Se dibuja la pantalla de color
        glUseProgram(colorPipeline.shaderProgram)


        if(player.isAlive == False):
            # La pantalla se pone roja
            sg.drawSceneGraphNodeShader(hudScene, colorPipeline, "transform", transparency, 2)

            # Dibujar Game Over
            palabra = sg.findNode(hudScene, "gameOver")
            palabra.transform = tr.matmul([tr.translate(transparency-0.95,0,0), tr.shearing(shearingEffect,0,0,0,0,0)])
             

            # Animacion de "game over" 
            if transparency > 1.0:
                transparency -= 3*delta
            else:
                shearingEffect -= 2*delta    
            shearingEffect -= 4.5*delta

            if shearingEffect <= 0:
                shearingEffect = 0    

        elif(controller.gameWon == True and player.isAlive == True):
            # Se dibuja la escena de victoria
            sg.drawSceneGraphNodeShader(victoryScreenNode, colorPipeline, "transform", victoryPos, 1)
            palabra = sg.findNode(hudScene, "victory")
            palabra.transform = tr.matmul([tr.translate(victoryPos-0.99,0.1,0),tr.shearing(0,shearingEffect,0,0,0,0)])

            # Aniamcion de "victory royale"
            if victoryPos > 1.0:
                victoryPos -= 5.5*delta
            else:
                shearingEffect -= 2*delta    

            shearingEffect -= 4.5*delta

            if shearingEffect <= 0:
                shearingEffect = 0  


        elif(player.isInfected == True):
            # Efecto de alucinacion de la infeccion
            transparency = 3.0
            sg.drawSceneGraphNodeShader(pantallaNode, colorPipeline, "transform", transparency, 0)

        # Once the drawing is rendered, buffe01rs are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    texScene.clear()
    hudScene.clear()

    glfw.terminate()