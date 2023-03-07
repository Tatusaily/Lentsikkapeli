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
    filtered_airports = random.sample(kentät, 5)
    print(f"DEBUG: filtered_airports: {filtered_airports}")
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

    # Otetaan game taulusta pelaajan tiedot ja tallennetaan ne muuttujiin.
    query = f"SELECT * FROM GAME WHERE screen_name = '{pelaajanimi}';"
    kursori.execute(query)
    tulos = kursori.fetchone()

    pelaajaid = tulos[0]
    points = tulos[1]
    P_location = tulos[2]
    pelaajanimi = tulos[3]
    salasana = tulos[4]

    # Otetaan pelaajan random kentät ja laitetaan ne muuttujiin.
    query = f"SELECT ICAO FROM randomport WHERE pelaaja_id = '{pelaajaid}';"
    kursori.execute(query)
    kentat = kursori.fetchall()
    P_kentat = []
    for kentta in kentat:
        P_kentat.append(kentta[0])

    # Jos on ihan uusi tunnus, niin asetetaan pelaaja random kentälle
    if P_location == "" or P_location is None:
        P_location = random.sample(P_kentat, 1)

    print(f"Hei, {pelaajanimi}. Sinulla on {points} pistettä.")
    print(f'Olet kentällä "{P_location}".')
    return


def pelaajaliike():
    global aihealueet
    global aihealue
    global P_location
    global P_kentat
    global points
    #TODO: anna käyttäjälle lentokentät
    uusilocation = str(input("Mihin lentokenttään haluat mennä?"))
    if kyssäfunktio() == True:
        points += 15
        print("Vastaus oikein :)")
        P_location = uusilocation
    else:
        points -= 10
        print("Vastaus väärin :(")
        if random.randint(0, 1) == 1:
            print("Lennät pyörremyrskyyn ja joudut satunnaiselle lentokentälle.")
            P_location = random.sample(P_kentat, 1)

    return

def kyssäfunktio():
    oikein = False
    global aihealueet
    # kysymystuple on -> ("missä jorma on?", Kotona, Lentokentällä, Ulkona, Piilossa, 2)
    # kyslista = [(kystuple),(kystuple),(kystuple)]
    # kysymyslistat siirretty pääohjelmaan
    print("Valitse aihealue:")
    n = 0
    for aihe in aihealueet:
        print(f"{n + 1}:{aihe[0]}")
        n += 1
    aihevalinta = abs(int(input()) - 1)
    if aihevalinta > len(aihealueet):
        aihevalinta = len(aihealueet)
    kyssälista = aihealueet[aihevalinta]
    kyssälista = kyssälista[1]

    kysymys = random.choice(kyssälista)
    aakkoset = ["a", "b", "c", "d"]
    print(kysymys[0])
    print(f"A) {kysymys[1]}     B) {kysymys[2]}\n"
          f"C) {kysymys[3]}     D) {kysymys[4]}")
    vastaus = str.lower(input())
    if vastaus.capitalize() == kysymys[kysymys[5]] or vastaus == aakkoset[kysymys[5]-1]:
        oikein = True
        aihealueet.remove(aihealueet[aihevalinta])  # jos vastaus on oikein, poistetaan aihe listasta
    return oikein


def highscore():
    #TODO: Tää loppuun
    # points on game-taulussa.
    # Oisko: SELECT screen_name, points FROM game ORDER BY points desc LIMIT 10;
    # sit print jotenkin kivasti
    print("HIGHSCORE")
    return


def päämenu():
    global gamestate
    global gameRunning
    global valinta
    print("TERVETULOA LENTOPELIIN!\n"
          "1: Aloita uusi peli.\n"
          "2: Jatka vanhaa peliä.\n"
          "3: Näytä Pisteet.\n"
          "4: Poistu pelistä.")
    valinta = int(input())
    if valinta == 1:
        gamestate = "uusipeli"
    elif valinta == 2:
        if tunnustarkistus() == True:
            # Tunnus on oikein ja voidaan jatkaa
            print("DEBUG Tunnus oikein! :)")
            gamestate = "jatkapeli"
        else:
            print("DEBUG Tunnus väärin! :(")
    elif valinta == 3:
        highscore()
    elif valinta == 4:      # Pelaaja menee menusta pois. Peliä ei ole kesken joten ei tarvitse tallentaa.
        gameRunning = False
        quit()
    return
def save():
    #TODO: pelajan tiedot tietokantaan
    # Varmaan voi vaan kattoo tosta noi alustetut arvot alempaa ja
    # Syöttää ne tietokantaan. Pitää kattoo et miten ne saa oikeelle paikalle.
    return


# Vakiot (Globaalit)
his_kyslista = []
geo_kyslista = []
pop_kyslista = []
finalboss_kyslista = []
# Alustetaan pelaaajalle arvot
# aihealueet on lista jossa on aihealueiden nimi, ja sitten osoite siihen listaan jossa ne kyssät on
# muodossa ("nimi", lista)
# tää on sen takii et kyssäfunktiossa voidaan sit kysyy dynaamisesti aihealue ja osataan ettii se lista
aihealueet = [("Populaatikulttuuri", pop_kyslista), ("Historia", his_kyslista),
              ("Maantieto", geo_kyslista)]
pelaajanimi = salasana = aihealue = P_location = ""
pelaajaid = points = 0
P_kentat = []

# Alkaa
gamestate = "päämenu"

# Pää looppi
gameRunning = True
while gameRunning == True:
    if gamestate == "päämenu":
        päämenu()   # Päämenusta voi aloittaa uuden pelin tai jatkaa vanhaa.
        # Tavallaan tää looppi on myös eräänlainen päämenu. Vähän hassua et se on myös funktio.
    elif gamestate == "uusipeli":
        uusipeli()  # Luodaan uusi pelaaja tietokantaan
        print("Uusi tunnus luotu.\n")
        valinta = str(input("Haluatko [P]alata takaisin valikkoon vai [J]atkaa peliä?"))
        if valinta == "J":
            gamestate = "jatkapeli"
        else:
            gamestate = "päämenu"
    elif gamestate == "jatkapeli":
        # TODO: Tähän vois ehkä laittaa jotain orientaatio tekstiä pelaajalle
        jatkapeli()             # Pelaajan tiedot ladataan tietokannasta
        print("Mitä haluat tehdä?\n"
              "1: Liiku uudelle lentokentälle.\n"
              "2: Poistu päävalikkoon.\n"
              "3: Lopeta peli.")
        valinta = int(input())
        if valinta == 1:
            pelaajaliike()      # Pelaaja liikkuu toiselle lentokentälle
        elif valinta == 2:
            gamestate = "päämenu"
        elif valinta == 3:
            gameRunning = False
        else: print("En ymmärtänyt.")

# Pelaaja valitsee poistumisen. Tallennetaan ja poistutaan.
print("Tallennetaan ja poistutaan.")
save()
print(f"Näkemiin, {pelaajanimi}.")
quit()
