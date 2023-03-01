#Tässä harjoitellaan napin tekemistä pygamella
import pygame
import sys
pygame.init()

#Vakiot
menufont = pygame.font.SysFont("Comic Sans", 35, True)
screenx = 800
screeny = 600
screen = pygame.display.set_mode((screenx, screeny))

# Tää CLASSI ei toiminut koska tein sen väärin :(
# Nyt se toimii, koska tein sen oikein :)
class MENUBUTTON:
    instances = []  # Lista johon lisätään viittaus kaikista napeista myöhemmin
    # Tää __init__ homma käy aina kun uusi olio luodaan
    def __init__(self,name, txt, x, y):
        self.__class__.instances.append(self)   # Lisätään nyt se viittaus
        self.name = name
        self.teksti = txt
        self.x = x
        self.y = y
        self.text = menufont.render(txt, True, "WHITE")                 # Luodaan teksti ja tehdään siitä kuva .renderillä
        self.text_rect = self.text.get_rect(center=(self.x, self.y))    # Luodaan tekstin kokoinen näkymätön laatikko ja laitetaan se napin sijaintiin
        screen.blit(self.text, self.text_rect)                          # Piirretään teksti laatikon sijaintiin

    # Funktiot joita napit laukaisee. Niihin viitataan napin nimellä joka annetaan kun olio luodaan
    def funktio(self):
        if self.name == "ylänappi":
            print("Painoit ylempää nappia.")
        if self.name == "alanappi":
            print("Painoit alempaa nappia.")

# Luodaan nappioliot
ylänappi = MENUBUTTON("ylänappi", "Oon ylempänä", screenx / 2, screeny / 4)
alanappi = MENUBUTTON("alanappi", "Oon alempana", screenx / 2, screeny / 2)


# Päälooppi
while True:
    # Eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:                            # klikatessa
            for instance in MENUBUTTON.instances:                           # nokkelasti loopataan kaikki napit läpi ja
                if instance.text_rect.collidepoint(pygame.mouse.get_pos()): # tarkistetaan että onko hiiri sen kohdalla
                    instance.funktio()                                      # ja suoritetaan sen funktio


    pygame.display.update()