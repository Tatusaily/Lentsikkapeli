// Funktiot
existingUser = async function(name, pass){
    /*
    const name = document.getElementById("username").value
    const pass = document.getElementById("password").value
     */
    const apiurl = `http://127.0.0.1:3000/getplayerdata/${name},${pass}`
    let apiresponse = await fetch(apiurl)
    apiresponse = await apiresponse.json()
    console.log(apiresponse)
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

    let result
    if (category === "general"){
        result = await generalTrivia()
        currentCategory = "general"
    }else{
        result = await mainTrivia(category)
        currentCategory = category
    }
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
    if (answer === rightanswer){
        isCorrect = true
        points += 100
    } else{isCorrect = false
        points -= 50
    }
    document.getElementById("points").innerText = points
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
    await fetch(`http://127.0.0.1:3000/moveplayer/${ICAO},${playername}`)
}



//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---
// Alustetaan Muutujia
let playername = "tat"
let points = 10000
document.getElementById("points").innerText = points
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
