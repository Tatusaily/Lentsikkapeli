import mysql.connector
# Funktiot tähän
def uusipeli():
    print("UUSIPELI")
    pelaajanimi = str(input("Anna pelaajanimesi: "))
    salasana = str(input("Anna salasanasi: "))
    yhteys = mysql.connector.connect(
        host='localhost', port=3306,
        database='flight_game', user='user1',
        password='sala1', autocommit=True)
    kursori = yhteys.cursor()

    # Tarkistetaan pelaajan nimi
    tarkista = f"SELECT count(*) as count FROM game WHERE screen_name = '{pelaajanimi}';"
    kursori.execute(tarkista)
    onkonimi = kursori.fetchone()
    if onkonimi[0] > 0:
        print("Pelaajanimi on jo käytössä. Yritä jotakin toista.")
    else:
        query = f"INSERT INTO game (screen_name, password) VALUES ('{pelaajanimi}', '{salasana}');"
        kursori.execute(query)
    kursori.close()
    yhteys.close()

    # Randomoidaan ne kentät ja tallennetaan ne jotenkin tietokantaan.
    return
def jatkapeli():
    print("JATKAPELI")
    # Pelaaja syöttää nimen, jos nimi on tietokannassa niin:
        # Pelaaja syöttää salasanan tai poistuu takaisin menuun
    return
def highscore():
    print("HIGHSCORE")
    return
def päämenu():
    print("TERVETULOA LENTOPELIIN!\n"
          "1: Aloita uusi peli.\n"
          "2: Jatka vanhaa peliä.\n"
          "3: Näytä Pisteet.\n"
          "4: Poistu pelistä.")
    valinta = input()
    if valinta == "1":
        uusipeli()
    elif valinta == "2":
        jatkapeli()
    elif valinta == "3":
        highscore()
    elif valinta == "4":
        gameRunning = False
        quit()
def save():
    # Jos pelaajan nimi ja salasana on tietokannassa niin tallennetaan edistys
    # Jos ei löydy, niin luodaan uusi rivi
    return

# Vakiot


# Alkaa
gamestate = "päämenu"

# Pää looppi
gameRunning = True
while gameRunning == True:
    if gamestate == "päämenu":
        päämenu()
    elif gamestate == "uusipeli":
        uusipeli()
    elif gamestate == "vanhapeli":
        jatkapeli()
