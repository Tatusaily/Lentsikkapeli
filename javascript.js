// Funktiot

// Ottaa tietokannasta syötetyillä arvoilla pelaajan tiedot. Jos pelaajaa ei löydy niin tekee jotain (ei tee vielä mitään jos ei löydy)
submitForm = async function(mode){
    const playerName = document.getElementById("player-name").value;
    const password = document.getElementById("password").value;

    if (playerName === '' || password === '') {
        alert('Please fill in both fields.');
        return false;
    }

    if(mode === "old"){
        const apiurl = `http://127.0.0.1:3000/getplayerdata/${playername},${password}`
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
            case 0: //LOGIN
                playername = apiresponse.name
                playerpoints = apiresponse.points
                playerlocation = apiresponse.location
                airportlocation = [apiresponse.airportlong, apiresponse.airportlat]
                break
            case 404:
                console.log("Error: 404")
        }
    } else if(mode === "new"){
        const apiurl = `http://127.0.0.1:3000/createplayer/${playerName},${password}`
        let apiresponse
        try{
            apiresponse = await fetch(apiurl)
            apiresponse = await apiresponse.json()
            console.log(apiresponse)
        }catch (error){console.log(error.message)}
        switch (apiresponse.error){
            case 0:
                playername = playerName
                break
            case 100:
                window.alert("Player with this name already exists.")
                return false
        }
    }
  document.getElementById('player-login').reset();
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
    if (answer === rightanswer){
        isCorrect = true
        playerpoints += 100 * diffMod
    } else{isCorrect = false
        playerpoints -= 50 * diffMod
    } playerpoints = Math.floor(playerpoints)
    document.getElementById("points").innerText = playerpoints
    return isCorrect
}
getEuropeAirports = async function(){
    let euAirportList = await fetch('http://127.0.0.1:3000/geteuropeairports')
    euAirportList = await euAirportList.json()
    console.log(euAirportList)
    return euAirportList
}
drawEuropeAirports = async function(){
    const euAirportList = await getEuropeAirports()
    console.log("saatiin kentät, aletaan piirtämään")
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
    console.log("kentät piirretty :)")
}
flyToAirport = async function(ICAO){
    let oldLocation = airportlocation
    // ICAO on uuden kentän ICAO
    // Päivittää pelaajan sijainnin tietokantaan ja ottaa uuden kentän koordinaatit samalla.
    airportlocation = await fetch(`http://127.0.0.1:3000/moveplayer/${ICAO},${playername}`)

    if (oldLocation !== ""){
        // Uusi - vanha
        // distance = vanhan ja uuden koordinaatin erotus
        let distance = [airportlocation[0]-oldLocation[0], airportlocation[1]-oldLocation[1]]
        // kuljettu etäisyys on vektorin pituus = sqrt(x^2 + y^2)
        distance = Math.sqrt(Math.pow(distance[0],2)+Math.pow(distance[1],2))
        console.log(playerpoints, distance)
        playerpoints =- distance*100
        console.log(playerpoints)
    }
}



//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---
// Alustetaan Muuttujia
let difficulty = ""
let playername = "testi"
let playerpoints = 1000
let playerlocation = "EFHK"
// Airportlocation on nykyisen lentokentän koordinaatit [longitude, latitude] muodossa
let airportlocation = [60.317222,24.963333]
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
// Näihin pitäis copyright-säännön mukaan laittaa joku "attribution" juttu mut ei laiteta ku se näyttää rumalta.
const lightlayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
const darklayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {maxZoom: 7,})
// Laitetaan layerit listaan ja linkataan se lista karttaan.
const maplayers = {"Lightmode": lightlayer, "Darkmode": darklayer}
const layerControl = L.control.layers(maplayers).addTo(map)
// Aloitetaan vaalealla layerilla
lightlayer.addTo(map)
const myIcon = L.icon({
    iconUrl: 'IMG/star.png',
    iconSize: [10, 10]
})
