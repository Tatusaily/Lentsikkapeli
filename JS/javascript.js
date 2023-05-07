// Funktiot

// Ottaa tietokannasta syötetyillä arvoilla pelaajan tiedot. Jos pelaajaa ei löydy niin tekee jotain
submitForm = async function(mode){
    const playerName = document.getElementById("player-name").value;
    const password = document.getElementById("password").value;
    document.getElementById('player-login').reset();
    // Jos kentät on tyhjiä
    if (playerName === '' || password === '') {
        alert('Please fill in both fields.');
        return false;
    }

    if(mode === "old"){
        const apiurl = `http://127.0.0.1:3000/getplayerdata/${playerName},${password}`
        let apiresponse
        try{
            // Otetaan vastaus ja jos ei ole tyhjä, niin tehdään siitä JSON
            apiresponse = await fetch(apiurl)
            apiresponse = await apiresponse.json()
            /* APIRESPONSE on muotoa:
                name:
                points:
                location: (ICAO)
                error:
             */
            console.log(apiresponse)
        }catch (error){console.log(error.message)}
        switch (apiresponse.error){
            case 0: //TIEDOT OIKEIN, LOGIN
                playername = apiresponse.name
                playerpoints = apiresponse.points
                playerlocation = apiresponse.location
                currentAirportCoords = [apiresponse.airportlong, apiresponse.airportlat]
                await drawEuropeAirports()
                return false
            case 404:
                console.log("Error: 404")
                break
        }
    } else if(mode === "new"){
        const apiurl = `http://127.0.0.1:3000/createplayer/${playerName},${password}`
        let apiresponse
        console.log(playerName, password)
        try{
            console.log("Mentiin tänne")
            apiresponse = await fetch(apiurl)
            console.log("1")
            apiresponse = await apiresponse.json()
            console.log("2")
            console.log(apiresponse)
        }catch (error){console.log(error.message)}
        switch (apiresponse.error){
            case 0:
                playername = playerName
                await drawEuropeAirports()
                return false
            case 100:
                window.alert("Player with this name already exists.")
                break
        }
    }
}
getQuestion = async function(category)  {
    // muutetaan category kutsuttavaan muotoon
    switch (category){
        case "History":
            category = "catHist"
            break;
        case "Mythology":
            category = "catMyth"
            break;
        case "Entertainment":
            category = "catEnte"
            break;
        case "Science":
            category = "catScie"
            break;
        case "General":
            category = "general"
            break;
    }
    //Tää vaihtaa vaikeustasoa pistemäärän mukaan
    if (playerpoints < 750){
        difficulty = "easy"
    } else if (playerpoints > 1250) {
        difficulty = "hard"
    } else {
        difficulty = "medium"
    }
    let result
    if (category === "general"){
        result = await generalTrivia(difficulty)
        currentCategory = "general"
    }else{
        result = await mainTrivia(category, difficulty)
        currentCategory = category
    }
    console.log(category, difficulty)
    const triviaArray = result.results[0]
    const triviaQuestion = triviaArray.question
    const correct = triviaArray.correct_answer
    let answers = triviaArray.incorrect_answers
    answers.push(correct)
    rightanswer = correct
    answers = answers.sort(() => 0.5 - Math.random())
    // DEBUG LOG
        console.log(triviaQuestion)
        console.log(answers)
        console.log(correct)
        //console.log(triviaArray)
    document.getElementById("question").innerHTML = triviaQuestion
    let counter = 0
    for (let button of answerButtons){
        button.innerHTML = answers[counter]
        counter += 1
    }

}
checkAnswer = async function(answer){
    let isCorrect
    let diffMod
    switch (difficulty) {
        case 'easy':
            diffMod = 0.75
            break;
        case 'hard':
            diffMod = 1.5
            break;
        default:
            diffMod = 1;
    }
    if (answer === rightanswer) {
        isCorrect = true
        playerpoints += 100 * diffMod
    } else {isCorrect = false
        playerpoints -= 50 * diffMod
    } playerpoints = Math.floor(playerpoints)
    document.getElementById("points").innerText = playerpoints
    if (playerpoints >= 2500) {
        // voitto, käyttäjän tallennus
    } else if (playerpoints <= 0){
        // häviö, uusi peli/poistu
    }

    else {
        return isCorrect;
    }
}
getEuropeAirports = async function(){
    let euAirportList = await fetch('http://127.0.0.1:3000/geteuropeairports')
    euAirportList = await euAirportList.json()
    // Laitetaan tiedot kaikista kentistä listaan myöhempää käyttöä varten
    euAirportList.forEach(airport =>{
        const port = {
            "icao": airport[2],
            "name": airport[3],
            "coords": [airport[0], airport[1]]
        }
        airportlist.push(port)
    })
    return euAirportList
}
drawEuropeAirports = async function(){
    const euAirportList = await getEuropeAirports()
    console.log("saatiin kentät, aletaan piirtämään")
    // Piirretään kentät ja annetaan niille popupit
    for (let airport of euAirportList){
        const button = document.createElement("button")
        button.innerHTML = "Fly to airport"
        button.onclick = function(){flyToAirport(airport[2])}
        let marker = L.marker([airport[0], airport[1]], {icon: myIcon}).addTo(map)

        // Pop-up sisältö
        let popDiv = document.createElement("div")
        let popText = document.createElement("p")
        popText.innerHTML = `Name: ${airport[3]}, ICAO: ${airport[2]}`
        popDiv.appendChild(popText)
        popDiv.appendChild(button)
        marker.bindPopup(popDiv).openPopup()
    }
    console.log(currentAirportCoords)
    currentMapMarker = L.marker([currentAirportCoords[0], currentAirportCoords[1]], {icon: currentIcon}).addTo(map)
    console.log("kentät piirretty :)")
    map.setView(currentAirportCoords)
}
flyToAirport = async function(ICAO){
    // ICAO on uuden kentän ICAO
    // Päivittää pelaajan sijainnin tietokantaan ja ottaa uuden kentän koordinaatit samalla.
    //currentAirportCoords = await fetch(`http://127.0.0.1:3000/moveplayer/${ICAO},${playername},${playerpoints}`)

    // Haetaan ICAOlla kenntä listasta ja otetaan sen koordinaatit uuden kentän koordinaatiksi
    for (let i = 0; i<airportlist.length; i++){
        if(airportlist[i].icao === ICAO){
            newAirportCoords = airportlist[i].coords
            break
        }
    }

    // Lasketaan etäisyys ja vähennetään pisteet
    if (currentAirportCoords !== ""){
        // Uusi - vanha
        // distance = vanhan ja uuden koordinaatin erotus
        let distance = [newAirportCoords[0]-currentAirportCoords[0], newAirportCoords[1]-currentAirportCoords[1]]
        console.log(distance)
        // kuljettu etäisyys on vektorin pituus = sqrt(x^2 + y^2)
        distance = Math.sqrt(Math.pow(distance[0],2)+Math.pow(distance[1],2))
        console.log("pts:",playerpoints, "dist:",distance)
        playerpoints = playerpoints - (distance*5 +10)
        console.log((distance*5 +10))
        console.log(playerpoints)
    }

    currentAirportCoords = newAirportCoords
    map.removeLayer(currentMapMarker)
    currentMapMarker = L.marker([currentAirportCoords[0], currentAirportCoords[1]], {icon: currentIcon}).addTo(map)
    map.setView(currentAirportCoords)
    getQuestion()
}



//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---
// Alustetaan Muuttujia
let airportlist = []
let difficulty = ""
let playername = "testi"
let playerpoints = 1000
let playerlocation = "EFHK"
let currentAirportCoords = [60.317222,24.963333]    // Longitude Latitiude
let newAirportCoords = []
let currentMapMarker
let rightanswer = ""
let currentCategory = ""
let answerButtons = document.getElementsByClassName("answer")
let categoryButtons = document.getElementsByClassName("category")

// Napit
for (let button of categoryButtons){
    const buttontext = button.innerHTML
    button.addEventListener("click", function (){getQuestion(buttontext)
    document.getElementById("buttons").style.display = "none"
    document.getElementById("question").style.display = "flex"
    document.getElementById("answerbox").style.display = "flex"})
}
for (let button of answerButtons){
    button.addEventListener("click", () => {
        checkAnswer(button.innerHTML)
        document.getElementById("buttons").style.display = "flex";
        document.getElementById("question").style.display = "none";
        document.getElementById("answerbox").style.display = "none";
    }
    )}

// Tehdään karttaolio "map".  "L" viittaa Leaflet-apiin.
let map = L.map("map", {renderer: L.canvas()})
map.setView([60.224168, 24.758141], 15)
// Luodaan eri layerit joita voi vaihtaa mapin oikeesta kulmasta.
// Näitä löytyy nimellä "tilelayer" tai "baselayer".
// const lightlayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
const darklayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
// const maplayers = {"Lightmode": lightlayer, "Darkmode": darklayer}
// const layerControl = L.control.layers(maplayers).addTo(map)
darklayer.addTo(map)
const myIcon = L.icon({
    iconUrl: '../IMG/star.png',
    iconSize: [10, 10]
})
const currentIcon = L.icon({
    iconUrl: '../IMG/star.png',
    iconSize: [30, 30]
})
