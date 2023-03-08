import mysql.connector

pelaajaid = 4
def compare_und_destroy():
    global aihealueet
    yhteys = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1', autocommit=True)
    kursori = yhteys.cursor()
äivämäärä on kansainvälinen Star Wars-päivä?", "4.5.", "20.4.", "11.11.", "3.2.", 1)]

aihealueet = [("Pop-kulttuuri", pop_kyslista), ("Historia", his_kyslista),
              ("Maantieto", geo_kyslista)]
compare_und_destroy()