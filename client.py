# (c) Vilhelm Prytz 2017
# Please do not edit this file, may corrupt your game installation.
# Tic Tac Toe Online

import sys

errMsg = ["Err 0: An error occured, but no error message found.",
          "Err 1: Only compatible with python 2. Please run with python 2.",
          "Err 2: A module is missing. Probably pygame? Install pygame and try again.",
          "Err 3: No internet connection! Is your internet down or our servers?"]


print("Welcome to Tic Tac Toe Online!")
print("Debug information will be printed in this console.")
print(" ")
global debug
debug = 0
ingame_fps = 60

from sys import version_info
py3 = version_info[0] > 2
if py3:
        print("FATAL ERROR: " + errMsg[1])
        import time
        time.sleep(5)
        quit(0)


# IMPORTANT FUNCTIONS
def quit_code():
        pygame.quit()
        print("Exiting Tic Tac Toe Online. Thank you for playing!")
        quit(0)

#init pygame
try:
        import pygame
except ImportError:
        print("FATAL ERROR: " + errMsg[2])
        import time
        time.sleep(5)
        quit(0)
import array
import csv
import urllib
import xmlrpclib
import time
import subprocess
import os.path

pygame.init()

#vars
display_width = 1280
display_height = 720
version = "a1.1"
mainServerAddr = ("http://us1-orfeus.tictactoe.mrkakisen.net:2016/")
# sq pos
# the cero
sqxPos = []
sqxPos.append("not used")
sqyPos = []
sqyPos.append("not used")

sqxPos.append(20)
sqxPos.append(220)
sqxPos.append(420)
sqxPos.append(20)
sqxPos.append(220)
sqxPos.append(420)
sqxPos.append(20)
sqxPos.append(220)
sqxPos.append(420)

sqyPos.append(20)
sqyPos.append(20)
sqyPos.append(20)
sqyPos.append(220)
sqyPos.append(220)
sqyPos.append(220)
sqyPos.append(420)
sqyPos.append(420)
sqyPos.append(420)


# some colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

green2 = (0,200,0)
red2 = (200,0,0)

# functions

def message_display(text, size, x, y):
        largeText = pygame.font.Font('game/freesansbold.ttf', size)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((x),(y))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def updateDisplay(bgColor):
        gameDisplay.fill(bgColor)
        pygame.display.update()
        clock.tick(60)
def button(msg, x, y, w, h, iColor, aColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y+h > mouse[1] > y:
                pygame.draw.rect(gameDisplay, aColor, (x,y,w,h))
                if click[0] == 1 and action != None:
                        #sloopy, not good :/
                        action()
                                
        else:
                pygame.draw.rect(gameDisplay, iColor, (x,y,w,h))

        smallText = pygame.font.Font("game/freesansbold.ttf", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)))
        gameDisplay.blit(textSurf, textRect)

def clickSquare():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # sq1
        if 20+200 > mouse[0] > 20 and 20+200 > mouse[1] > 20:
                if click[0] == 1:
                        return "clicked_sq1"
        # sq2 x                    x       y                  y
        elif 220+200 > mouse[0] > 220 and 20+200 > mouse[1] > 20:
                if click[0] == 1:
                        return "clicked_sq2"
        # sq3
        if 420+200 > mouse[0] > 420 and 20+200 > mouse[1] > 20:
                if click[0] == 1:
                        return "clicked_sq3"
        # sq4
        elif 20+200 > mouse[0] > 20 and 220+200 > mouse[1] > 220:
                if click[0] == 1:
                        return "clicked_sq4"
        # sq5
        elif 220+200 > mouse[0] > 220 and 220+200 > mouse[1] > 220:
                if click[0] == 1:
                        return "clicked_sq5"
        # sq6
        elif 420+200 > mouse[0] > 420 and 220+200 > mouse[1] > 220:
                if click[0] == 1:
                        return "clicked_sq6"
        # sq7
        elif 20+200 > mouse[0] > 20 and 420+200 > mouse[1] > 420:
                if click[0] == 1:
                        return "clicked_sq7"
        # sq8
        elif 220+200 > mouse[0] > 220 and 420+200 > mouse[1] > 420:
                if click[0] == 1:
                        return "clicked_sq8"
        # sq9
        elif 420+200 > mouse[0] > 420 and 420+200 > mouse[1] > 420:
                if click[0] == 1:
                        return "clicked_sq9"
        else:
                return "noClick"

# get connection to main server
import errno
from socket import error as socket_error

print("Trying to establish connection to server...")

mainServer = xmlrpclib.ServerProxy(mainServerAddr)

try:
        pingReply = mainServer.getPing()
except socket_error as serr:
        if serr.errno != errno.ECONNREFUSED:
                raise serr
        print("FATAL ERROR: " + errMsg[3])
        import time
        time.sleep(5)
        quit(0)
if (pingReply == "pong"):
        print("Connection successful!")
else:
        print("FATAL ERROR: " + errMsg[3])
        import time
        time.sleep(5)
        quit(0)   

# load images / assets
print("Loading assets..")
# images
circleImage = pygame.image.load("game/circle.png")
xImage = pygame.image.load("game/x.png")

# setup window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe Online [" + version + "]")
clock = pygame.time.Clock()
pygame.display.set_icon(xImage)
print("Window setup done.")

# remove tmp
f = open("tmp_gl_quitMainMenu.tmp", "w")
f.write("False")
f.close()

# main menu
def mainMenu():
        print("Main menu module init")
        exitMainMenu = False
        while exitMainMenu is False:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_code()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        exitMainMenu = True
                gameDisplay.fill(white)
                
                button("Join Session", display_width/2-100,display_height/2,400,50, red, red2, joinSessionLoop)
                button("Create Session", display_width/2-100,display_height/2+100,400,50, green, green2, createSessionLoop)

                message_display("Tic Tac Toe Online", 72, display_width/2-100, display_height/2-100)
                
                pygame.display.update()
                clock.tick(60)
                
                f = open("tmp_gl_quitMainMenu.tmp", "r")
                if (f.read() == "True"):
                        f.close()
                        f = open("tmp_gl_quitMainMenu.tmp", "w")
                        f.write("False")
                        f.close()
                        exitMainMenu = True
                        print("Shouldn't be in main menu. Quitting to game loop!")
                else:
                        f.close()
                

# main game loop
def gameLoop():
        PlayerIsP1 = False
        PlayerIsP2 = False
        print("Game loop module init")
        print("Fetchig p2key / session")
        f = open("tmp_playerState.tmp", "r")
        playerState = f.read()
        f.close()
        if (playerState == "P1"):
                f = open("tmp_session.tmp", "r")
                session = f.read()
                f.close()

                PlayerIsP1 = True

                print("Fetching gamedata once - P1")
                print("Current info: I'm P1. Session: " + session)
                sq = mainServer.getGameData(session)
                sessionStatus = mainServer.getSessionStatus(session)
                mainServer.gameReady(session, "isP1")
        if (playerState == "P2"):
                f = open("tmp_p2key.tmp", "r")
                p2key = f.read()
                f.close()

                f = open("tmp_session.tmp", "r")
                session = f.read()
                f.close()
                
                PlayerIsP2 = True

                print("Fetching gamedata once - P2")
                print("Current info: I'm P2. Session: " + session + " This is p2key: " + p2key)
                sq = mainServer.getGameData(session)
                sessionStatus = mainServer.getSessionStatus(session)
                mainServer.gameReady(session, p2key)
        connectTick = 0
        exitGameLoop = False
        while exitGameLoop is False:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_code()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        print("EXIT!")
                                        exitGameLoop = True
                gameDisplay.fill(white)
                # basic rectangle shape (full box = 600x600 big)
                pygame.draw.rect(gameDisplay, black, [20,20,620,620])
                pygame.draw.rect(gameDisplay, white, [30,30,600,600])

                # draw lines (downwards)
                pygame.draw.rect(gameDisplay, black, [220,20,10,620])
                pygame.draw.rect(gameDisplay, black, [420,20,10,620])

                # draw lines (vert)
                pygame.draw.rect(gameDisplay, black, [20,220,620,10])
                pygame.draw.rect(gameDisplay, black, [20,420,620,10])

                # who's turn will be drawn at the end (due to flickering bug?)

                # draw the plays
                # sq 1
                if (sq[1] == "X"):
                        gameDisplay.blit(xImage, (20,20))
                if (sq[1] == "O"):
                        gameDisplay.blit(circleImage, (20,20))
                # sq 2
                if (sq[2] == "X"):
                        gameDisplay.blit(xImage, (220,20))
                if (sq[2] == "O"):
                        gameDisplay.blit(circleImage, (220,20))
                # sq 3
                if (sq[3] == "X"):
                        gameDisplay.blit(xImage, (420,20))
                if (sq[3] == "O"):
                        gameDisplay.blit(circleImage, (420,20))
                # sq 4
                if (sq[4] == "X"):
                        gameDisplay.blit(xImage, (20,220))
                if (sq[4] == "O"):
                        gameDisplay.blit(circleImage, (20,220))
                # sq 5
                if (sq[5] == "X"):
                        gameDisplay.blit(xImage, (220,220))
                if (sq[5] == "O"):
                        gameDisplay.blit(circleImage, (220,220))
                # sq 6
                if (sq[6] == "X"):
                        gameDisplay.blit(xImage, (420,220))
                if (sq[6] == "O"):
                        gameDisplay.blit(circleImage, (420,220))
                # sq 7
                if (sq[7] == "X"):
                        gameDisplay.blit(xImage, (20,420))
                if (sq[7] == "O"):
                        gameDisplay.blit(circleImage, (20,420))
                # sq 8
                if (sq[8] == "X"):
                        gameDisplay.blit(xImage, (220,420))
                if (sq[8] == "O"):
                        gameDisplay.blit(circleImage, (220,420))
                # sq 9
                if (sq[9] == "X"):
                        gameDisplay.blit(xImage, (420,420))
                if (sq[9] == "O"):
                        gameDisplay.blit(circleImage, (420,420))

                clickReply = clickSquare()

                if (PlayerIsP1 == True):
                        if (sessionStatus == "p1Turn"):
                                if (clickReply == "clicked_sq1"):
                                        mainServer.makeMove(session, "isP1", 1)
                                        sq[1] = "X"
                                elif (clickReply == "clicked_sq2"):
                                        mainServer.makeMove(session, "isP1", 2)
                                        sq[2] = "X"
                                elif (clickReply == "clicked_sq3"):
                                        mainServer.makeMove(session, "isP1", 3)
                                        sq[3] = "X"
                                elif (clickReply == "clicked_sq4"):
                                        mainServer.makeMove(session, "isP1", 4)
                                        sq[4] = "X"
                                elif (clickReply == "clicked_sq5"):
                                        mainServer.makeMove(session, "isP1", 5)
                                        sq[5] = "X"
                                elif (clickReply == "clicked_sq6"):
                                        mainServer.makeMove(session, "isP1", 6)
                                        sq[6] = "X"
                                elif (clickReply == "clicked_sq7"):
                                        mainServer.makeMove(session, "isP1", 7)
                                        sq[7] = "X"
                                elif (clickReply == "clicked_sq8"):
                                        mainServer.makeMove(session, "isP1", 8)
                                        sq[8] = "X"
                                elif (clickReply == "clicked_sq9"):
                                        mainServer.makeMove(session, "isP1", 9)
                                        sq[9] = "X"
                elif (PlayerIsP2 == True):
                        if (sessionStatus == "p2Turn"):
                                if (clickReply == "clicked_sq1"):
                                        mainServer.makeMove(session, p2key, 1)
                                        sq[1] = "O"
                                elif (clickReply == "clicked_sq2"):
                                        mainServer.makeMove(session, p2key, 2)
                                        sq[2] = "O"
                                elif (clickReply == "clicked_sq3"):
                                        mainServer.makeMove(session, p2key, 3)
                                        sq[3] = "O"
                                elif (clickReply == "clicked_sq4"):
                                        mainServer.makeMove(session, p2key, 4)
                                        sq[4] = "O"
                                elif (clickReply == "clicked_sq5"):
                                        mainServer.makeMove(session, p2key, 5)
                                        sq[5] = "O"
                                elif (clickReply == "clicked_sq6"):
                                        mainServer.makeMove(session, p2key, 6)
                                        sq[6] = "O"
                                elif (clickReply == "clicked_sq7"):
                                        mainServer.makeMove(session, p2key, 7)
                                        sq[7] = "O"
                                elif (clickReply == "clicked_sq8"):
                                        mainServer.makeMove(session, p2key, 8)
                                        sq[8] = "O"
                                elif (clickReply == "clicked_sq9"):
                                        mainServer.makeMove(session, p2key, 9)
                                        sq[9] = "O"

                # draw player turn at the end
                if (PlayerIsP1 == True):
                        gameDisplay.blit(xImage, (720,80))
                        if (sessionStatus == "p1Turn"):
                                message_display("Your turn!", 32, 780, 40)
                        else:
                                message_display("Opponents turn!", 32, 780, 40)
                                

                elif (PlayerIsP2 == True):
                        gameDisplay.blit(circleImage, (720,80))
                        if (sessionStatus == "p2Turn"):
                                message_display("Your turn!", 32, 780, 40)
                        else:
                                message_display("Opponents turn!", 32, 780, 40)


                # update the screen
                pygame.display.update()
                clock.tick(ingame_fps)

                connectTick = connectTick+1
                if (connectTick == 60):
                        connectTick = 0

                        sq = mainServer.getGameData(session)
                        print("|-----------|")
                        print("| " + str(sq[1]) + " | " + str(sq[2]) + " | " + str(sq[3]) + " |")
                        print("| " + str(sq[4]) + " | " + str(sq[5]) + " | " + str(sq[6]) + " |")
                        print("| " + str(sq[7]) + " | " + str(sq[8]) + " | " + str(sq[9]) + " |")
                        print("|-----------|")
                        sessionStatus = mainServer.getSessionStatus(session)
                        print("Sessionstauts: " + sessionStatus + " ||| Current player1: " + str(PlayerIsP1) + " Current player2: " + str(PlayerIsP2) + " PLAYERSTATE: " + playerState)
                        if  (sessionStatus == "p1Win" or sessionStatus == "p2Win" or sessionStatus == "tieWin"):
                                print("GAME END! " + sessionStatus)
                                exitGameLoop = True

                                winLoop = False
                                quitTick = 0
                                while winLoop is False:
                                        quitTick = quitTick+1
                                        gameDisplay.fill(white)
                                        if (sessionStatus == "p1Win"):
                                                message_display("Player 1 wins!", 72, display_width/2-100, display_height/2-100)
                                                gameDisplay.blit(xImage, (display_width/2-100, display_height/2))
                                        elif (sessionStatus == "p2Win"):
                                                message_display("Player 2 wins!", 72, display_width/2-100, display_height/2-100)
                                                gameDisplay.blit(circleImage, (display_width/2-100, display_height/2))
                                        elif (sessionStatus == "tieWin"):
                                                message_display("Tie!", 72, display_width/2-100, display_height/2-100)
                                        else:
                                                message_display("Error! Did nobody win?", 72, display_width/2-100, display_height/2-100)

                                        pygame.display.update()
                                        clock.tick(ingame_fps)

                                        if (quitTick == 180):
                                                winLoop = True

                                print("Going back to main menu. Goodbye ingame!")

def createSessionLoop():
        print("Create Session loop module init")
        print("Generating new session...")
        newSession = mainServer.createSession()
        print("Session generated. ID: " + newSession)
        connectTime = 0
        exitSessionLoop = False
        while exitSessionLoop is False:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_code()
                gameDisplay.fill(white)
                message_display("Ask your game partner to enter code " + newSession, 20, display_width/2, display_height/2)
                pygame.display.update()
                clock.tick(60)

                connectTime = connectTime+1
                if (connectTime == 120):
                        status = mainServer.getSessionStatus(newSession)
                        if (status == "waitingP2"):
                                connectTime = 0
                        elif (status == "allJoined"):
                                print("P2 has joined!")
                                f = open("tmp_session.tmp", "w")
                                f.write(newSession)
                                f.close()

                                f = open("tmp_gl_quitMainMenu.tmp", "w")
                                f.write("True")
                                f.close()

                                f = open("tmp_playerState.tmp", "w")
                                f.write("P1")
                                f.close()
                                
                                exitSessionLoop = True
                                gl_quitMainMenu = True
                        else:
                                print("INVALID REPLY!!")
                                exitSessionLoop = True
def joinSessionLoop():
        print("Join Session loop module init")

        timerOn = False
        letter = []
        letter.append("not used")
        letter.append("")
        letter.append("")
        letter.append("")
        letter.append("")
        letter.append("")
        letter.append("")
        letter.append("")
        currentLetter = 1
        
        exitSessionLoop = False
        while exitSessionLoop is False:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_code()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_a:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "A"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_b:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "B"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_c:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "C"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_d:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "D"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_e:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "E"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_f:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "F"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_g:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "G"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_h:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "H"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_i:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "I"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_j:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "J"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_k:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "K"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_l:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "L"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_m:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "M"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_n:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "N"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_o:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "O"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_p:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "P"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_q:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "Q"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_r:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "R"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_s:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "S"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_t:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "T"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_u:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "U"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_v:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "V"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_w:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "W"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_x:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "X"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_y:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "Y"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_z:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "Z"
                                                currentLetter = currentLetter+1
                                # NUMBERS
                                if event.key == pygame.K_0:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "0"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_1:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "1"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_2:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "2"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_3:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "3"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_4:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "4"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_5:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "5"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_6:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "6"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_7:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "7"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_8:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "8"
                                                currentLetter = currentLetter+1
                                if event.key == pygame.K_9:
                                        if (currentLetter == 7):
                                                print("Only 6 chars allowed.")
                                        else:
                                                letter[currentLetter] = "9"
                                                currentLetter = currentLetter+1
                                # DELETE (BACKSPACE)
                                if event.key == pygame.K_BACKSPACE:
                                        if (letter[currentLetter] == "" and currentLetter != 1):
                                                currentLetter = currentLetter-1
                                                letter[currentLetter] = ""
                                        elif (currentLetter == 1):
                                                currentLetter = 1
                                                letter[currentLetter] = ""
                                        else:
                                                currentLetter = currentLetter-1
                                                letter[currentLetter] = ""

                                # hit enter
                                if event.key == pygame.K_RETURN:
                                        if (currentLetter == 7):
                                                session = allLetters
                                                if (mainServer.sessionExists(session) == True and mainServer.getSessionStatus(session) == "waitingP2"):
                                                        p2key = mainServer.joinSession(session)
                                                        exitSessionLoop = True
                                                        print("Session joined.")

                                                        f = open("tmp_p2key.tmp", "w")
                                                        f.write(p2key)
                                                        f.close()

                                                        f = open("tmp_session.tmp", "w")
                                                        f.write(session)
                                                        f.close()

                                                        f = open("tmp_gl_quitMainMenu.tmp", "w")
                                                        f.write("True")
                                                        f.close()

                                                        f = open("tmp_playerState.tmp", "w")
                                                        f.write("P2")
                                                        f.close()
                                                else:
                                                        timerOn = True
                                                        timer = 0
                                        else:
                                                print("not all filled")
                                
                gameDisplay.fill(white)
                message_display("Enter session below", 20, display_width/2, display_height/2)
                message_display("____________________", 20, display_width/2, display_height/2+40)
                allLetters = letter[1] + letter[2] + letter[3] + letter[4] + letter[5] + letter[6]
                message_display(allLetters, 20, display_width/2, display_height/2+32)
                # if not found
                if (timerOn == True):
                        timer = timer+1
                        message_display("Session not found! Try again.", 20, display_width/2, display_height/2+70)
                        if (timer == 120):
                                timerOn = False

                pygame.display.update()
                clock.tick(60)

quitEndlessMain = False
while quitEndlessMain is False:
        mainMenu()
        gameLoop()

quit_code()