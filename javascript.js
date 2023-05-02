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
    console.log(apiresponse)
    return apiresponse
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
    }else{isCorrect = false}
    return isCorrect
}
//---------------PÄÄOHJELMA----------------
//---TÄÄ SUORITETAAN AINA KUN HTML AUKEE---

let rightanswer = ""
let currentCategory = ""
let categoryButtons = document.getElementsByClassName("category")
for (let button of categoryButtons){
    const buttontext = button.innerHTML
    button.addEventListener("click", function (){getQuestion(buttontext)})
}
/*
categoryButtons.forEach(button => {
    const buttontext = button.innerHTML
    button.addEventListener("click", function (){getQuestion(buttontext)})
})*/
//categoryButton.addEventListener("click", function(){getQuestion("general")})



// Tehdään karttaolio "map".  "L" viittaa Leaflet-apiin.
let map = L.map("map")
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


/* testi
laittaa merkin koordinaattiin (60, 24)
vois testaa laittaa for -loopilla läjän näitä
    vaikka tietokannasta?
    tarkotus ois vetää sieltä python koodista API-kutsulla
*/
//L.marker([60, 24]).addTo(map)
