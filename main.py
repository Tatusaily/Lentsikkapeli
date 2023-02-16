import pygame

#Funktiot tähän
def newplayer():
    #Tähän koodia joka tekee uuden pelaajan sql kantaan.
    #Pelaajan tiedot on game-taulussa
    return


pygame.init()
#Vakiot
screenXRes = 800
screenYRes = 600
screenResolution = (screenXRes, screenYRes)



#Pää looppi
gameRunning = True
while gameRunning == True:
    for event in pygame.event.get():
        if event.type == pygame .QUIT:
            pygame.quit()
            quit(print("Sammutaan koska quit"))

