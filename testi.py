filtered_airports = (1, 2, 3, 4, 5)




def jatkolento():
    for i in filtered_airports:
        print(*filtered_airports[i])
        input("Valitse lentokenttä: ")

# tässä poistetaan näkyvistä jo vierailtu lentokenttä

# X lähintä?
from geopy import distance
filtered_airports = [(1, "kentän nimi", 3, 4),(2, "asdf", 10, 2),(3, "asdf", 5, 1),(4, "asdf", 6, 21),(5, "asdf", 5, 1)]
def lähimmät():
    nykyinen = (12, 40)
    lista = []
    global filtered_airports
    for airport in filtered_airports:
        lentis = (airport[2], airport[3])
        dista = round(distance.distance(nykyinen, lentis).km, 2)
        lista.append((dista, airport[0], airport[1]))
        lista.sort()
    # 140m, icao, kentän nimi
    return (lista)
lahimmat = lähimmät()
print(lahimmat)