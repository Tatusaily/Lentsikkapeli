import mysql.connector
import random
# Funktiot tähän
def uusipeli():
    print("UUSIPELI")
    yhteys = mysql.connector.connect(
        host='localhost', port=3306,
        database='flight_game', user='user1',
        password='sala1', autocommit=True)
    kursori = yhteys.cursor()

    # Otetaan pelaajalta nimi ja salasana, tarkistetaan ne ja laitetaan ne kantaan
    while True:
        pelaajanimi = str(input("Anna pelaajanimesi: "))
        salasana = str(input("Anna salasanasi: "))
        # Tarkistetaan pelaajan nimi
        query = f"SELECT count(*) as count FROM game WHERE screen_name = '{pelaajanimi}';"
        kursori.execute(query)
        onkonimi = kursori.fetchone()
        if onkonimi[0] > 0:
            print("Pelaajanimi on jo käytössä. Yritä jotakin toista.")
        else:
            query = f"INSERT INTO game (screen_name, password) VALUES ('{pelaajanimi}', '{salasana}');"
            kursori.execute(query)
            break

    # Randomoidaan ne kentät ja tallennetaan ne jotenkin tietokantaan. Tää ottaa kaikki kenttätyypit
    query = f"SELECT ident FROM airport WHERE continent= 'EU' AND(NOT iso_country = 'RU');"
    kursori.execute(query)
    kentät = kursori.fetchall()
    global filtered_airports
    filtered_airports = random.sample(kentät, 5)
    query = f"SELECT id FROM game WHERE screen_name = '{pelaajanimi}' AND password = '{salasana}';"
    kursori.execute(query)
    pelaajaID = kursori.fetchone()
    for airport in filtered_airports:
        query = f"REPLACE INTO randomport(pelaaja_id, ICAO) VALUES ('{pelaajaID[0]}', '{airport[0]}');"
        kursori.execute(query)

    kursori.close()
    yhteys.close()
    return

def jatkapeli():
    print("JATKAPELI")
    # Pelaaja syöttää nimen, jos nimi on tietokannassa niin:
        # Pelaaja syöttää salasanan tai poistuu takaisin menuun
    while True:
        pelaajanimi = input("Anna käyttäjänimi: ")
        salasana = input("Anna salasana: ")
        yhteys = mysql.connector.connect(
            host='localhost', port=3306,
            database='flight_game', user='user1',
            password='sala1', autocommit=True)
        kursori = yhteys.cursor()
        query = f"SELECT screen_name, password FROM game WHERE screen_name = '{pelaajanimi}';"
        kursori.execute(query)
        tulos = kursori.fetchall()
        for tunnus in tulos:
            if tunnus[0] == pelaajanimi and tunnus[1] == salasana:
                oikein = True
        if oikein == True: break
        else:
            print("Väärä tunnus tai salasana")
    # Tässä vaihessa tunnus on varmistettu
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
        print("Uusi tunnus luotu.")
        print(filtered_airports)
        gamestate = "jatkapeli"
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
    elif gamestate == "jatkapeli":
        jatkapeli()
