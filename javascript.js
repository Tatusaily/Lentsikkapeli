existingUser = async function(name, pass){
    const host = '127.0.0.1:3000'
    const playerdata = `/getplayerdata/${name},${pass}`
    const apiurl = `${host}+${playerdata}`

    const apiresponse = await fetch(apiurl)
    return apiresponse
}

//PÄÄOHJELMA
// Tehdään karttaolio "map". "L" viittaa Leaflet-apiin.
let map = L.map("map").setView([60.224168, 24.758141], 15);
// Luodaan eri layerit joita voi vaihtaa mapin oikeesta kulmasta.
// Näitä löytyy nimellä "tilelayer" tai "baselayer".
// Näihin pitäis copyright-säännön mukaan laittaa joku "attribution" juttu mut ei laiteta ku se näyttää rumalta.
const lightlayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
const darklayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
// Laitetaan layerit listaan ja linkataan se lista karttaan.
const maplayers = {"Lightmode": lightlayer, "Darkmode": darklayer}
const layerControl = L.control.layers(maplayers).addTo(map)
// Aloitetaan vaalealla layerilla
lightlayer.addTo(map)


/* testi
laittaa merkin koordinaattiin (60, 24)
vois testaa laittaa for -loopilla läjän näitä
    vaikka tietokannasta?
    tarkotus ois vetää sieltä python koodista API-kutsulla
*/
L.marker([60, 24]).addTo(map)
