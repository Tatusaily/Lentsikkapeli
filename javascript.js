existingUser = async function(){
    const name = document.getElementById("username").value
    const pass = document.getElementById("password").value
    /*
    const proxy = 'https://users.metropolia.fi/~ilkkamtk/proxy.php?url='
    const apiurl = `${proxy}http://127.0.0.1:3000/getplayerdata/${name},${pass}`
     */

    // tulee joku cors error
    // toimii oikein jos laittaa apirulin suoraan selaimen URLiin.
    const apiurl = `http://127.0.0.1:3000/getplayerdata/${name},${pass}`
    console.log(apiurl)
    const apiresponse = await fetch(apiurl)
    const apiresponse2 = await apiresponse.json()
    console.log(apiresponse2)
    return apiresponse2
}

// Yksi funktio jolla voi kutsua eri kysymykset. Varmaan helpoin käyttää tätä napeissa
getQuestion = async function(category){
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
    // TODO Tähän sit koodia joka syöttää ne kysymykset sinne front-endiin
    document.getElementById("question").innerHTML = triviaQuestion
    let counter = 0
    for (let button of answerButtons){
        button.innerHTML = answers[counter]
        counter += 1
    }

}
/*
getGeneralQuestion = async function(){
    // otetaan kyssä
    currentCategory = "general"
    const randomQuestion = await generalTrivia()
    const question = randomQuestion.results[0].question
    const correct = randomQuestion.results[0].correct_answer
    let answers = randomQuestion.results[0].incorrect_answers
    answers.push(correct)
    rightanswer = correct
    answers = answers.sort(() => 0.5 - Math.random())
    // DEBUG LOG
        console.log(question)
        console.log(answers)
        console.log(correct)
        console.log(randomQuestion)
}
getMainQuestion = async function(category){
    // otetaan kyssä
    const mainQuestion = await mainTrivia(category)
    const questionArray = mainQuestion.results[0]
    const questionText = questionArray.question
    const correct = questionArray.correct_answer
    let answers = questionArray.incorrect_answers
    answers.push(correct)
    rightanswer = correct
    answers = answers.sort(() => 0.5 - Math.random())
}*/
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
    console.log("saatiin")
    for (let airport of euAirportList){
        let marker = L.marker([airport[0], airport[1]], {icon: myIcon}).addTo(map)
        let popupContent = `Name: ${airport[3]}, ICAO: ${airport[2]}`
        marker.bindPopup(popupContent).openPopup()
    }
    console.log("tehty")
}




//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---
let points = 10000
document.getElementById("points").innerText = points
let rightanswer = ""
let currentCategory = ""
let answerButtons = document.getElementsByClassName("answer")
let categoryButtons = document.getElementsByClassName("category")
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


/*
categoryButtons.forEach(button => {
    const buttontext = button.innerHTML
    button.addEventListener("click", function (){getQuestion(buttontext)})
})*/
//categoryButton.addEventListener("click", function(){getQuestion("general")})



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
// Piirretään EU kentät kartalle
//drawEuropeAirports()


/* testi
laittaa merkin koordinaattiin (60, 24)
vois testaa laittaa for -loopilla läjän näitä
    vaikka tietokannasta?
    tarkotus ois vetää sieltä python koodista API-kutsulla
*/
//L.marker([60, 24]).addTo(map)
