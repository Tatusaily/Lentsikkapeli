#Tässä harjoitellaan napin tekemistä pygamella
import pygame
import sys
pygame.init()

#Vakiot
menufont = pygame.font.SysFont("Comic Sans", 35, True)
screenx = 800
screeny = 600
screen = pygame.display.set_mode((screenx, screeny))

""" Tää CLASSI ei tee mitään kun en saanut sitä toimimaan :(
class MENUBUTTON:
    #Nappi jossa on tekstiä
    #Nappi haluaa tekstin ja sijainnin
    def __init__(self, txt, x, y):
        text = menufont.render(txt, True, "WHITE")

    def draw(self, x, y):
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
"""


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                print("KOSKEE!")

    menufont = pygame.font.SysFont("Comic Sans", 35, True)
    text = menufont.render("Paina mua!", True, "WHITE")                  #tekee tekstistä surfacen, koko päätellään fontin mukaan
    text_rect = text.get_rect(center=(screenx/2, screeny/3))       #tekee text-surfacen kokoinen suorakulmio ja laitetaan se tiettyyn kohtaan
    screen.blit(text, text_rect)                                   #piirretään "text"-pinta "text_rect" kulmion sijaintiin.



    pygame.display.update()