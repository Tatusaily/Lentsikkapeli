'use strict';
// nää on niitä aihealueita joita käytetään yleissivistyksessä eli näist ei saa muuta ku pisteitä
const generalTriArr = [9, 21, 22, 26, 27]
// tää ottaa randomilla sen noist arrayn numeroista
const randomGen = Math.floor(Math.random() * generalTriArr.length);
// tää on se funktio mut ei toimi vielä kokonaan, en tiiä pitääks tän olla async (varmaan pitää)
// pitää viel lisää joku jolla saa ne sit sinne html tiedostoihin
async function generalTrivia() {
  const apiUrl = `https://opentdb.com/api.php?amount=1&category=${generalTriArr[randomGen]}&difficulty=medium&type=multiple`;
  try {
    const result = await fetch(apiUrl)
    const jsonResult = await result.json()
    return jsonResult
  } catch(error) {
    console.log(error.message)
  }
}

async function mainTrivia(category) {
  let catNum
  let random
  switch(category){
    case "catHist":
      catNum = 23
      break;
    case "catMyth":
      catNum = 20
      break;
    case "catEnte":
      const entTriArr = [15, 10, 11, 14, 16, 29, 31, 32]
      random = Math.floor(Math.random() * entTriArr.length);
      catNum = entTriArr[random]
      break;
    case "catScie":
      const sciTriArr = [17, 18, 19, 30]
      random = Math.floor(Math.random() * sciTriArr.length);
      catNum = sciTriArr[random]
      break;
    default:
      console.log("moi")
  }
  const apiUrl = `https://opentdb.com/api.php?amount=1&category=${catNum}&difficulty=medium&type=multiple`;
  try {
    const result = await fetch(apiUrl)
    const jsonResult = await result.json()
    console.log(jsonResult)
    return jsonResult
  } catch(error) {
    console.log(error.message)
  }
}

