// nää on niitä aihealueita joita käytetään yleissivistyksessä eli näist ei saa muuta ku pisteitä
let generalTriArr = [9, 21, 22, 26, 27]
// tää ottaa randomilla sen noist arrayn numeroista
let random = Math.floor(Math.random() * generalTriArr.length);
// tää on se funktio mut ei toimi vielä kokonaan, en tiiä pitääks tän olla async (varmaan pitää)
// pitää viel lisää joku jolla saa ne sit sinne html tiedostoihin
async function generalTrivia() {
  const apiUrl = `https://opentdb.com/api.php?amount=1&category=${generalTriArr[random]}&difficulty=medium&type=multiple`;
  try {
    const result = await fetch(apiUrl)
    const jsonResult = await result.json()
    return jsonResult
  } catch(error) {
    console.log(error.message)
  }
}
