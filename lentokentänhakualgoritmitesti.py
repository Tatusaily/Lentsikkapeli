import mysql.connector

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='sala1',
         autocommit=True
         )
def GetAirport(contsa, konetype):
    contsa = contsa.upper()
    query = f"SELECT name, type, latitude_deg, longitude_deg FROM airport WHERE continent= '{contsa}' "
    if konetype == "Medium":
        query += f"AND type = 'Medium_Airport' or type = 'Large_Airport';"
    elif konetype == "Large":
        query += f"AND type = 'Large_Airport';"
    elif konetype == "Small":
        query += f"AND or type = 'Small_Airport' type = 'Medium_Airport' or type = 'Large_Airport';"

    kursori = yhteys.cursor()
    kursori.execute(query)
    tulos = kursori.fetchall()
    return tulos

conttis = input("Anna manner: ")
airplanetype = "Medium"

tulos = GetAirport(conttis, airplanetype)



print(tulos)
print(len(tulos))