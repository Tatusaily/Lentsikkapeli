#Tässä harjoitellaan napin tekemistä pygamella
import pygame
import sys
pygame.init()

#Vakiot
menufont = pygame.font.SysFont("Comic Sans", 35, True)
screenx = 800
screeny = 600
screen = pygame.display.set_mode((screenx, screeny))

#Tää CLASSI ei toiminut koska tein sen väärin :(
#Nyt se toimii, koska tein sen oikein :)
class MENUBUTTON:
    instances = []
    def __init__(self,name, txt, x, y):
        self.__class__.instances.append(self)
        self.name = name
        self.teksti = txt
        self.x = x
        self.y = y
        self.text = menufont.render(txt, True, "WHITE")
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        screen.blit(self.text, self.text_rect)

    def funktio(self):
        if self.name == "ylänappi":
            print("Painoit ylempää nappia.")
        if self.name == "alanappi":
            print("Painoit alempaa nappia.")

ylänappi = MENUBUTTON("ylänappi", "Oon ylempänä", screenx / 2, screeny / 4)
alanappi = MENUBUTTON("alanappi", "Oon alempana", screenx / 2, screeny / 2)


#Päälooppi
while True:
    #Eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for instance in MENUBUTTON.instances:
                if instance.text_rect.collidepoint(pygame.mouse.get_pos()):
                    instance.funktio()

            """
            if ylänappi.text_rect.collidepoint(pygame.mouse.get_pos()):
                ylempinappi()
            if alanappi.text_rect.collidepoint(pygame.mouse.get_pos()):
                alempinappi()
            """

    pygame.display.update()