import mysql.connector

def compare_und_destroy():
    global aihealueet
    yhteys = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1', autocommit=True)
    kursori = yhteys.cursor()
    query = f"select * from category;"
    kursori.execute(query)
    compare = kursori.fetchall()
    vittu = []
    for x in aihealueet:
        if aihealueet[0] == compare [1]:
            aihealueet.remove(x)
        print(x)
    yhteys.close()
    kursori.close()
    return

his_kyslista = [("Minä vuonna Google perustettiin?", "1995", "1998", "2000", "1997", 2),
                ("Milloin suomi itsenäistyi?", "Eilen", "1914", "1917", "2002", 3),
                ("Kuka maalasi Mona Lisan?", "Akseli Gallen-Kallela", "Vesa", "Banksy", "Leonardo da Vinci", 4)]

geo_kyslista = [("Mikä on Belgian pääkaupunki", "Pariisi", "Antwerp", "Bryssel", "Gent", 3),
                ("Missä maassa K2-vuori sijaitsee?", "Pakistanissa", "Intiassa", "Norjassa", "Kiinassa", 1),
                ("Mikä maa ei kuulu joukkoon?", "Ruotsi", "Suomi", "Norja", "Tanska", 2)]

pop_kyslista = [("Mitä akronyymi " + "'ong' " + "tarkoittaa?", "Oh my god", "Ei mitään", "On god", "Onko nägyny?", 3),
                ("Kuka näistä ei ole tunnettu muusikko?", "Kanye West", "markoboy87", "Post Malone", "Taylor swift", 2),
                ("Mikä päivämäärä on kansainvälinen Star Wars-päivä?", "4.5.", "20.4.", "11.11.", "3.2.", 1)]

aihealueet = [("Pop-kulttuuri", pop_kyslista), ("Historia", his_kyslista),
              ("Maantieto", geo_kyslista)]
compare_und_destroy()