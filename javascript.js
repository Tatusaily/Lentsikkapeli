// Funktiot

// Ottaa tietokannasta syötetyillä arvoilla pelaajan tiedot. Jos pelaajaa ei löydy niin tekee jotain (ei tee vielä mitään jos ei löydy)
existingUser = async function(){
    const name = document.getElementById("username")
    const pass = document.getElementById("password")
    const apiurl = `http://127.0.0.1:3000/getplayerdata/${name.value},${pass.value}`
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
            /* Nyt tää vaihtaa sivua kokonaan, mut se ei oikeen sovi
            Jos vaihtaa sivua ja sit sijoittaa muuttujien arvoja johonkin
            HTML elementtiin joita ei oo vanhassa sivussa,
            tulee erroria koska sitä elementtiä ei löydy */
            document.location.href = "testi.html"
            playername = apiresponse.name
            playerpoints = apiresponse.points
            playerlocation = apiresponse.location
            break
        case 404:
            console.log("Error: 404")
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
    // ICAO on uuden kentän ICAO

    await fetch(`http://127.0.0.1:3000/moveplayer/${ICAO},${playername}`)

}



//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---
// Alustetaan Muuttujia
let difficulty = ""
let playername = "testi"
let playerpoints = 200
let playerlocation = "testi"
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
