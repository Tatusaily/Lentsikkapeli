import pygame

pygame.init()

# reso aka määritellään näytön "pinta-ala" - en tiedä käyttääkö pygame pikseleitä mut näil mennää
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Pelin nimi
pygame.display.set_caption("Lentsikka")

# Fontti ja koko (testataan sega fonttia)
font = pygame.font.Font("SEGA.ttf", 50)

# värit tausta musta, fontti valkoinen
white = (255, 255, 255)
black = (0, 0, 0)

high_scores = [] # lista johon pelaajien pistemäärä tallennetaan kun peli on päättynyt

# päävalikon funktio fr fr
def main_menu():
    # menun tekstit aka mitä valintavaihtoehtoja tulee menuun
    new_game_text = font.render("Uusi Peli", True, white)
    load_game_text = font.render("Lataa Peli", True, white)
    save_game_text = font.render("Tallenna Peli", True, white)
    high_scores_text = font.render("Näytä Huipputulokset", True, white)
    quit_text = font.render("Lopeta", True, white)

    # tekstin sijainnit ruudulla tähän
    new_game_position = (screen_width // 2 - new_game_text.get_width() // 2, screen_height // 2 - 200)
    load_game_position = (screen_width // 2 - load_game_text.get_width() // 2, screen_height // 2 - 100)
    save_game_position = (screen_width // 2 - save_game_text.get_width() // 2, screen_height // 2)
    high_scores_position = (screen_width // 2 - high_scores_text.get_width() // 2, screen_height // 2 + 100)
    quit_position = (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 200)

    # piirretään teksti ruudulle ehkä näin?
    screen.fill(black)
    screen.blit(new_game_text, new_game_position)  # nää ehkä vaatii surface.blit?
    screen.blit(load_game_text, load_game_position)
    screen.blit(save_game_text, save_game_position)
    screen.blit(high_scores_text, high_scores_position)
    screen.blit(quit_text, quit_position)

    # päivitetään näkymä
    pygame.display.update()

    # looppi millä valikot pysyvät näkyvissä valintaan asti. yritetään saada valinta tehtyä hiirellä.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if new_game_position[0] < mouse_pos[0] < new_game_position[0] + new_game_text.get_width() \
                        and new_game_position[1] < mouse_pos[1] < new_game_position[1] + \
                        new_game_text.get_height():
                    # uusi peli
                    new_game()
                elif load_game_position[0] < mouse_pos[0] < load_game_position[0] + load_game_text.get_width() \
                        and load_game_position[1] < mouse_pos[1] < load_game_position[1] + load_game_text.get_height():
                    # ladataan vanha tallennus
                    load_game()
                elif save_game_position[0] < mouse_pos[0] < save_game_position[0] + save_game_text.get_width() \
                        and save_game_position[1] < mouse_pos[1] < save_game_position[1] + save_game_text.get_height():
                    # tämä nyt on edelleen täällä, mutta poistetaan finaaliversiosta. Testailen vain saanko näitä
                    # toimimaan.
                    save_game()
                elif high_scores_position[0] < mouse_pos[0] < high_scores_position[0] + high_scores_text.get_width() \
                        and high_scores_position[1] < mouse_pos[1] < high_scores_position[1] + \
                        high_scores_text.get_height():
                    # listataan high scores
                    high_scores = []
def new_game():
    print("new game")
    return

def load_game():
    print("load game")
    return

def save_game():
    print("seivgeimrofl")
    return

main_menu()