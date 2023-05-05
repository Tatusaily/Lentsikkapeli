const overlay = document.getElementById("overlay");
const floatBox = document.getElementById("float-box");
const closeButton = document.getElementById("close-button");

function showFloatBox() {
  overlay.classList.add("show");
}

function hideFloatBox() {
  overlay.classList.remove("show");
}

document.addEventListener("click", function(event) {
  if (event.target === overlay) {
    hideFloatBox();
  }
});

closeButton.addEventListener("click", hideFloatBox);
