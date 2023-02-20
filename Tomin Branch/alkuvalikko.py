# lista high scores
high_scores = []


# Jonkinlainen menu esim.
def game_menu():
    print("Tervetuloa pelaamaan lentsikkapeliä!")
    print("1. Uusi peli")
    print("2. Lataa tallennettu peli")
    print("3. Tallenna peli")  # lisäsin tähän, mutta tämä pitää laittaa vaihtoehdoksi vasta kun peli on käynnissä
    print("4. Näytä huipputulokset")
    print("5. Lopeta")


# Uusi peli
def select_new_game():
    print("Aloitetaan uusi peli...")
    # käynnistetään uusi peli, kysytään pelaajan nimi, tallennetaan pelaajan nimi databaseen ja arvotaan aloituspiste


# Lataa tallennus
def load_old_save():
    print("Ladataan tallennettu peli...")
    # tähän koodi mikä hakee vanhan tallennuksen pelaajan nimen perusteella ja käynnistää pelin siitä pisteestä missä
    # peli tallennettiin.


# Tallenna peli
def save_game():
    print("Tallennetaan...")
    # tähän koodi mikä tallentaa pelaajan tiedot (kerätyt pisteet, sijainnin ym)
    # pelaajan nimen perusteella tietokantaan ja palaa päämenuun


# Tällä näytetään high scores lista
def display_high_scores():
    print("High Scores:")
    for score in high_scores:
        print(score)
        # tähän sitten tarkemmin missä muodossa (nimi, pisteet tms)

# tämä käynnistää pelin ja siirtyy menuun
def start_game_menu():
    while True:
        game_menu()
        choice = input("Anna valinta: ")
        if choice == "1":
            select_new_game()
        elif choice == "2":
            load_old_save()
        elif choice == "3":
            save_game()
        elif choice == "4":
            display_high_scores()
        elif choice == "5":
            print("Nähdään taas!")
            break
        else:
            print("Väärä valinta.")


# päävalikko
start_game_menu()