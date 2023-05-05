function submitForm() {
  let playerName = document.getElementById("player-name").value;
  let password = document.getElementById("password").value;

  if (playerName === '' || password === '') {
    alert('Please fill in both fields.');
    return false;
  }
  console.log('Player Name: ' + playerName);
  console.log('Password: ' + password);

  // reset
  document.getElementById('player-login').reset();
  return false;
}