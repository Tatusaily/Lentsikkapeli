'use strict';
// nää on niitä aihealueita joita käytetään yleissivistyksessä eli näist ei saa muuta ku pisteitä
const generalTriArr = [9, 21, 22, 26, 27]
// tää ottaa randomilla sen noist arrayn numeroista
const randomGen = Math.floor(Math.random() * generalTriArr.length);

let apiUrl
async function generalTrivia(difficulty) {
  apiUrl = `https://opentdb.com/api.php?amount=1&category=${generalTriArr[randomGen]}&difficulty=${difficulty}&type=multiple`;
  try {
    const result = await fetch(apiUrl)
    const jsonResult = await result.json()
    return jsonResult
  } catch(error) {
    console.log(error.message)
  }
}

async function mainTrivia(category, difficulty) {
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
      console.log("Encountered an error. No such category.")
  }
  apiUrl = `https://opentdb.com/api.php?amount=1&category=${catNum}&difficulty=${difficulty}&type=multiple`;
  console.log(apiUrl)
  try {
    const result = await fetch(apiUrl)
    const jsonResult = await result.json()
    //console.log(jsonResult)
    return jsonResult
  } catch(error) {
    console.log(error.message)
  }
}

