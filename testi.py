filtered_airports = [(1, "kentän nimi"),(2, "asdf"),(3, "asdf"),(4, "asdf"),(5, "asdf")]

print("Olet lentokentällä X. Tehtäväsi on Y.")

def liike():
    for i in filtered_airports:
        print(*i)
        input("Valitse seuraava kohde: ")
    return(f"lennetään kohteeseen {filtered_airports - 1}...")
    # tähän jotain lisää
liike()

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

kyssäri = (1:ads,2:ads,3:asd,4:asd,0)
vastaus = "ads",a,1-1
