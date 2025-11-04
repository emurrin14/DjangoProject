//Header Hamburger Open and Close
const hamBtn = document.getElementById("hamburgerOpen");
const hamClose = document.getElementById("hamburgerClose");
const hamMenuContiner = document.getElementById('hamburgerMenuContainer');
const hamMenuOverlay = document.getElementById('hamburgerMenuOverlay');

function toggleHamburger() {
    hamBtn.classList.toggle("hamburgerActive");
    hamClose.classList.toggle("hamburgerCloseActive");
}
hamBtn.addEventListener("click", toggleHamburger);
hamClose.addEventListener("click", toggleHamburger);