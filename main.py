## resource site opengameart.org (image,music, effet sonnor)
import random

import pygame
from pygame import mixer
#initialiser avec pygame exentielle
pygame.init()
mixer.init()

# Créer une fenetre pour afficher le jeu
# display affichage
# set_mode definir mode affichage 1er parametre taille fenetre en pixel
window = pygame.display.set_mode((800, 600))
#  modifier le titre et l'icon
pygame.display.set_caption("Demon Loda")
# icon site sur iconfinder.com
# charger et retorner ficher image
windowIcon = pygame.image.load("alien.png")
pygame.display.set_icon(windowIcon)

# On charge l'image du joueur
player = pygame.image.load("player.png")
# convertir en rectangle
playerRect = player.get_rect()
# stocker la position du joueur à l'ecran
posX = 350
posY = 480

# variable vitesse du deplacement
playerSpeed = 5

# on charge l'image backgound
background = pygame.image.load("bg.png")

# on charge l'image laser
laser = pygame.image.load("laser.png")
laserRect = laser.get_rect()
laserSpeed = 4
posLaserX = 0
posLaserY = -100
# creation variable boolean tirer est vrai
canShoot = True

# L'OVNI
#ovni = pygame.image.load("ufo.png")
#ovniRect = ovni.get_rect()
#posOvniX = random.randint(0, 750)
#posOvniY = 50

ovni = [] # image
ovniRect = [] # rect
posOvniX = [] # posX
posOvniY = [] # posY
ovniSpeed = [] # vitesse
nbOvni = 4

# Texte
score = 0
font = pygame.font.Font('future.ttf', 28)
txtPos = 10

gameOver = False
fontOver = pygame.font.Font('future.ttf', 48)
posOverX = 250
posOverY = 300

# Musique
#mixer.music.load("sfx_laser.mp3")
# Jouer la musique
#parametre -1 music en boucle
#mixer.music.play(-1)

# Boucle de generation des ovni
for i in range(nbOvni):
    ovni.append(pygame.image.load("ufo.png"))
    ovniRect.append(ovni[i].get_rect())
    posOvniX.append(random.randint(1, 750))
    posOvniY.append(random.randint(0, 300))
    ovniSpeed.append(3)

# fonction de detection de collision
def collision(rectA, rectB):
    if rectB.right < rectA.left:
        # rectB est à gauche
        return False
    if rectB.bottom < rectA.top:
        # rectB est au-dessus
        return False
    if rectB.left > rectA.right:
        # rectB est à droit
        return False
    if rectB.top > rectA.bottom:
        # rectB est en-dessous
        return False
    # Dans tous les autres cas il y a collision
    return True

# Pour definir les FPS (image par seconde)
# Création horloge
clock = pygame.time.Clock()

# boucle de jeu
# en 60 image par seconde exemple (rafreshissement par image)
running = True
while running:
    # couleur de l'ecran
    # colorer notre fenetre parm(rouge,vert,bleu) site color.adobe.com/fr/create/color-wheel
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    ##gestion des evenemet
    # recuperer les event avec pygame
    # je check tous les evenement (clavier/souris)
    for event in pygame.event.get():
        # Est ce que l'utilisateur appuie sur une touche ?
        # retourne la touche appuier dans pressed
        pressed = pygame.key.get_pressed()

        # on test si l'utilisateur appuie sur la croix du fenetre
        if event.type == pygame.QUIT:
            # on quite le jeu
            running = False

        # on test les fleches du clavier
        # Exemple de deplacement cran par cran
        if event.type == pygame.KEYDOWN:
            # De quelle touche s'agit-il ?
            # if event.key == pygame.K_LEFT:
                # Le joueur a appuyé sur la fleche à gauche
                # posX -= 50
            # if event.key == pygame.K_RIGHT:
                # Le joueur a ppuyé sur la fleche à droit
                # posX += 50
            # Detection barre d'espace pour tirer le laser
            if event.key == pygame.K_SPACE and canShoot:
                # Son du laser charger # Son du laser charger
                laserSfx = mixer.Sound("sfx_laser2.ogg")
                laserSfx.play()
                canShoot = False
                posLaserX = posX + 45
                posLaserY = posY - 50

    # Gestion du deplacement du joueur à l'ecran
    if pressed[pygame.K_LEFT] and posX > 0:
        posX -=playerSpeed
    if pressed[pygame.K_RIGHT] and posX < 700:
        posX +=playerSpeed


    # Affichier joueur
    # on aplique cette position au rectangle
    playerRect.topleft = (posX, posY)
    # on affiche l'image du joueur dans la fenetre  de jeu
    # blit pour definir notre source qu'on veut afficher à l'inteieur de certe fenetre
    window.blit(player, playerRect)

    #Afficher le laser
    posLaserY -= laserSpeed
    laserRect.topleft = (posLaserX, posLaserY)
    window.blit(laser, laserRect)
    if posLaserY < -40:
        canShoot = True

    # Afficher des ovni
    # deplacer l'ovni de droit à gauche
    for i in range(nbOvni):
        posOvniX[i] -= ovniSpeed[i]
        ovniRect[i].topleft = (posOvniX[i], posOvniY[i])
        window.blit(ovni[i], ovniRect[i])
        if posOvniX[i] < 0 or posOvniX[i] > 750:
            ovniSpeed[i] = -ovniSpeed[i]
            posOvniY[i] += 50

        # Y a t il collision entre le laser et l'ovni
        if collision(laserRect, ovniRect[i]):
            posOvniY[i] = 10000
            posLaserY = -500
            score += 1
            soundWin = mixer.Sound("sfx_hit.ogg")
            soundWin.play()

        # Y a il collision entre le l'ovni et le joueur
        if collision(playerRect, ovniRect[i]):
            posY = 10000
            canShoot = False
            gameOver = True

    # Affichage du score
    # rendu du text
    scoreText = font.render("Score : " + str(score), True, (255, 255, 255))
    window.blit(scoreText, (txtPos, txtPos))

    if gameOver == True:
        overText = fontOver.render("GAME OVER ", True, (255, 255, 255))
        window.blit(overText, (posOverX, posOverY))

    # on dessine / mettre à jour le contenu de l'ecran
    pygame.display.flip()
    # definir le nombre d'image par seconde
    clock.tick(60)



# quiter pygame
pygame.quit()