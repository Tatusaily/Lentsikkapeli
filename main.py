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
        global pelaajanimi
        global salasana
        pelaajanimi = str(input("Anna pelaajanimesi: "))
        salasana = str(input("Anna salasanasi: "))
        # Tarkistetaan pelaajan nimi
        query = f"SELECT count(*) as count FROM game WHERE screen_name = '{pelaajanimi}';"
        kursori.execute(query)
        onkonimi = kursori.fetchone()
        #TODO: Nimi/Salasana kombo
        if onkonimi[0] > 0:
            print("Pelaajanimi on jo käytössä. Yritä jotakin toista.")
        else:
            query = f"INSERT INTO game (screen_name, password) VALUES ('{pelaajanimi}', '{salasana}');"
            kursori.execute(query)
            break

    # Randomoidaan ne kentät ja tallennetaan ne jotenkin tietokantaan. Tää ottaa kaikki kenttätyypit
    query = f"SELECT ident, name FROM airport WHERE continent= 'EU' AND(NOT iso_country = 'RU');"
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
def tunnustarkistus():
    print("TUNNUSTARKISTUS")
    oikein = False
    global pelaajanimi
    global salasana
    pelaajanimi = str(input("Anna käyttäjänimi: "))
    salasana = str(input("Anna salasana: "))
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
    # Tässä vaihessa tunnus on varmistettu
    return oikein
def jatkapeli():
    yhteys = mysql.connector.connect(
        host='localhost', port=3306,
        database='flight_game', user='user1',
        password='sala1', autocommit=True)
    kursori = yhteys.cursor()
    global pelaajanimi
    """
    jos pelaajan sijainti on 0
        laitetaan käyttäjä satunnaiselle kentälle randomport-taulusta
    jos ei
        käyttäjä jatkaa siitä missä on (game/location)
        muistuttaa
    """
    query = f"SELECT * FROM GAME WHERE screen_name = '{pelaajanimi}';"
    kursori.execute(query)
    tulos = kursori.fetchone()

    # Tehdään kaikista pelaajan tiedoista globaaleja muuttujia myöhempää varten.
    global pelaajaid
    pelaajaid = tulos[0]
    global points
    points = tulos[1]
    global P_location
    P_location = tulos[2]
    pelaajanimi = tulos[3]
    global salasana
    salasana = tulos[4]
    query = f"SELECT ICAO FROM randomport WHERE pelaaja_id = '{pelaajaid}';"
    global P_kentat
    P_kentat = []
    kursori.execute(query)
    kentat = kursori.fetchall()
    for kentta in kentat:
        P_kentat.append(kentta[0])

    if P_location == 0:
        P_location = random.sample(P_kentat, 1)
    return


def pelaajaliike():
    global P_location
    #TODO tää funktio kokonaan :(
    #pelaaaja on jossain ja se menee johonnkin.
    #menon jälkeen tulee kyssäri?
    uusilocation = str(input("Anna uusi location"))

    # kyssät tähän
    if kyssäfunktio() == True:
        points += 100
        print("Vastaus oikein :)")
        P_location = uusilocation
    else:
        points -= 1
        print("Vastaus väärin :(")
        P_location = random.sample(P_kentat, 1)
    return


def kyssäfunktio():

    return


def highscore():
    print("HIGHSCORE")
    return


def päämenu():
    global gamestate
    print("TERVETULOA LENTOPELIIN!\n"
          "1: Aloita uusi peli.\n"
          "2: Jatka vanhaa peliä.\n"
          "3: Näytä Pisteet.\n"
          "4: Poistu pelistä.")
    valinta = int(input())
    if valinta == 1:
        uusipeli()
        print("Uusi tunnus luotu.")
        print(filtered_airports)
        gamestate = "jatkapeli"
    elif valinta == 2:
        if tunnustarkistus() == True:
            # Tunnus on oikein ja voidaan jatkaa
            print("Oikein! :)")
            gamestate = "jatkapeli"
        else:
            print("Tunnus väärin! :(")

    elif valinta == 3:
        highscore()
    elif valinta == 4:
        gameRunning = False
        quit()


def save():
    # Jos pelaajan nimi ja salasana on tietokannassa niin tallennetaan edistys
    # Jos ei löydy, niin luodaan uusi rivi
    return


# Vakiot
pelaajanimi = ""
salasana = ""
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
        #TODO Tää loppuun
        jatkapeli()
        pelaajaliike()

"""        "Mitä haluut"
        liike()
            kyssäri
        gamestate = "päämenu"""
