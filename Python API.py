import mysql.connector
import random
import json
from flask import Flask
from flask_cors import CORS
# API rakennus
app = Flask(__name__)
CORS(app)

# getplayerdata palauttaa määritellyn pelaajan tiedot tietokannasta
@app.route('/getplayerdata/<playername>,<password>')
def getplayerdata(playername, password):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    query = f"SELECT screen_name, points, location " \
            f"FROM game " \
            f"WHERE screen_name= '{playername}' and password= '{password}';"
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)
    sqlresult = sqlcursor.fetchone()
    if sqlresult is not None:
        playerdata = {
            "name": sqlresult[0],
            "points": sqlresult[1],
            "location": sqlresult[2],
            "airportlong": "",
            "airportlat": "",
            "error": 0
        }
        location = playerdata["location"]
        query = f"SELECT latitude_deg, longitude_deg " \
                f"FROM airport " \
                f"WHERE ident= '{location}' ;"
        sqlcursor = sqlconnection.cursor()
        sqlcursor.execute(query)
        sqlresult = sqlcursor.fetchone()
        playerdata["airportlong"] = sqlresult[0]
        playerdata["airportlat"] = sqlresult[1]
        return playerdata
    elif sqlresult is None:
        return {"error": 404}


@app.route('/geteuropeairports')
def geteuropeairports():
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    query = f"SELECT latitude_deg, longitude_deg, ident, name " \
            f"FROM airport " \
            f"WHERE continent='EU' AND type='large_airport' AND NOT iso_country='RU';"
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)
    sqlresult = sqlcursor.fetchall()
    '''
    randnum = random.sample(range(len(sqlresult)), 200)
    airfields = []
    for num in randnum:
        airfields.append(sqlresult[num])
    '''
    airfields = sqlresult
    return airfields


@app.route('/moveplayer/<icao>,<name>,<points>')
def moveplayer(icao, name, points):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    # Päivitetään pelaajan sijainti
    query = f"UPDATE GAME " \
            f"SET location = '{icao}', points = '{points}' " \
            f"WHERE screen_name = '{name}' ;"
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)
    return{"ok": 1}


@app.route('/createplayer/<playername>,<password>')
def createplayer(playername, password):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    query = f"SELECT screen_name " \
            f"FROM game " \
            f"WHERE screen_name = '{playername}';"
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)
    sqlresult = sqlcursor.fetchone()
    if sqlresult is None:
        # Pelaajaa ei ole.
        query = f"INSERT into game (screen_name, password) " \
                f"VALUES ('{playername}','{password}');"
        sqlcursor = sqlconnection.cursor()
        sqlcursor.execute(query)
        return {"error": 0}
    elif sqlresult is not None:
        print("Pelaaja koitti tehdä jo olemasssa olevan pelaajan")
        return {"error": 100}


@app.route('/deleteplayer/<name>')
def deleteplayer(name):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    query = f"DELETE FROM game " \
            f"WHERE screen_name = '{name}';"
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)


# Pääohjelma käynnistää flask-taustapalvelun localhostiin
if __name__ == '__main__':

    app.run(use_reloader=True, host='127.0.0.1', port=3000)