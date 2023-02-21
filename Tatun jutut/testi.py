import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ei kinkku karoliina")
clocktick = pygame.time.Clock()

def teepalikka (kokox,kokoy,color,posx,posy):
    surface = pygame.Surface((kokox, kokoy))
    surface.fill(color)
    screen.blit(surface,(posx,posy))
    return

test_surface = pygame.Surface((100,200))
test_surface.fill("red")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface,(700,0))
    teepalikka(100,200,"blue",0,200)

    pygame.display.update()
    clocktick.tick(60)