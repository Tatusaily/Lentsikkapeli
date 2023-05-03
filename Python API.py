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
    playerdata = {
        "name": sqlresult[0],
        "points": sqlresult[1],
        "location": sqlresult[2]
    }
    return playerdata


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
    return sqlresult


@app.route('/moveplayer/<icao>,<name>')
def moveplayer(icao, name):
    sqlconnection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='user1',
        password='sala1',
        autocommit=True
    )
    query = f"UPDATE GAME " \
            f"SET location = '{icao}' " \
            f"WHERE screen_name = '{name}' ;"
    print(query)
    sqlcursor = sqlconnection.cursor()
    sqlcursor.execute(query)
    return "Player Moved"


# Pääohjelma käynnistää flask-taustapalvelun localhostiin
if __name__ == '__main__':

    app.run(use_reloader=True, host='127.0.0.1', port=3000)