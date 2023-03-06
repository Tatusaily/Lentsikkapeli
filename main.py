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

    # Kivat global muuttujat :)
    global pelaajanimi
    global pelaajaid
    global points
    global P_location
    global salasana
    global P_kentat

    """
    jos pelaajan sijainti on NULL
        laitetaan käyttäjä satunnaiselle kentälle randomport-taulusta
    jos ei
        käyttäjä jatkaa siitä missä on (game/location)
        muistuttaa
    """

    query = f"SELECT * FROM GAME WHERE screen_name = '{pelaajanimi}';"
    kursori.execute(query)
    tulos = kursori.fetchone()

    # Talletaan queryllä saadut tiedot pelaaja tietoihin
    pelaajaid = tulos[0]
    points = tulos[1]
    P_location = tulos[2]
    pelaajanimi = tulos[3]
    salasana = tulos[4]

    # Otetaan pelaajan random kentät ja laitetaan ne muuttujaan muistiin
    query = f"SELECT ICAO FROM randomport WHERE pelaaja_id = '{pelaajaid}';"
    kursori.execute(query)
    kentat = kursori.fetchall()
    P_kentat = []
    for kentta in kentat:
        P_kentat.append(kentta[0])

    # Jos on ihan uusi tunnus, niin asetetaan pelaaja random kentälle
    if P_location == "" or P_location == None:
        P_location = random.sample(P_kentat, 1)

    print(f"Hei, {pelaajanimi}. Sinulla on {points} pistettä.")
    print(f'Olet kentällä "{P_location}".')
    return


def pelaajaliike():
    global aihealueet
    global aihealue
    global P_location
    global P_kentat

    #TODO Mitä vittua?
    uusilocation = str(input("Mihin lentokenttään haluat mennä?"))
    aihealue = str.lower(input(f"Jäljellä olevat aihealueet: {aihealueet}\n"
                               f"Valitse aihealue: "))
    if kyssäfunktio(aihealue) == True:
        points += 100
        print("Vastaus oikein :)")
        aihealueet.remove(aihealue)
        P_location = uusilocation
    else:
        points -= 10
        print("Vastaus väärin :(")
        P_location = random.sample(P_kentat, 1)

    return


def kyssäfunktio():
    oikein = False
    # kysymystuple on -> ("missä jorma on?", Kotona, Lentokentällä, Ulkona, Piilossa, 2)
    # kyslista = [(kystuple),(kystuple),(kystuple)]
    his_kyslista = []
    geo_kyslista = []
    pop_kyslista = [("Missä jOrma on?", "Kotona", "Lentokentällä", "Ulkona", "Piilossa", 2),
                ("Missä Matti on?", "Kotona", "Lentokentällä", "Ulkona", "Piilossa", 2),
                ("Missä Heikki on?", "Kotona", "Lentokentällä", "Ulkona", "Piilossa", 2)]
    finalboss_kyslista = []

    #TODO: IF/ELSE lause joka ottaa valitun aihealueen ja kysyy siitä ne kysymykset!

    kysymys = random.choice(his_kyslista)
    aakkoset = ["a", "b", "c", "d"]
    print(kysymys[0])
    print(f"A) {kysymys[1]}     B) {kysymys[2]}\n"
          f"C) {kysymys[3]}     D) {kysymys[4]}")
    vastaus = str.lower(input())
    if vastaus.capitalize() == kysymys[kysymys[5]] or vastaus == aakkoset[kysymys[5]-1]:
        oikein = True
    return oikein


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
        print("Uusi tunnus luotu.\n")
        print(f"DEBUG: {filtered_airports}")
        valinta = str(input("Haluatko [P]alata takaisin valikkoon vai [J]atkaa peliä?"))
        if valinta == "J":
            gamestate = "jatkapeli"
            # TODO: Tähän vois laittaa jotain pelin aloitus tekstiä
        else:
            gamestate = "päämenu"

    elif valinta == 2:
        # TODO: pelaajan SQL Dump tähän. Ei kyl tarvii? Ne näyttää tulevan ihan kivasti kun ne alustetaan tossa alhaalla.
        if tunnustarkistus() == True:
            # Tunnus on oikein ja voidaan jatkaa
            print("DEBUG Tunnus oikein! :)")
            gamestate = "jatkapeli"
        else:
            print("DEBUG Tunnus väärin! :(")

    elif valinta == 3:
        highscore()
    elif valinta == 4:
        gameRunning = False
        quit()


def save():
    #TODO: pelajan tiedot tietokantaan
    return


# Vakiot (Globaalit)
# Alustetaan pelaaajalle arvot
aihealueet = ["Populaatikulttuuri", "Historia", "Maantieto"]
pelaajanimi = salasana = aihealue = P_location = ""
pelaajaid = points = 0
P_kentat = []

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
