document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("saleCountdownContainer");
  if (!container) return;

  const startDate = new Date(container.dataset.startDate);
  const endDate = new Date(container.dataset.endDate);
  const statusEl = document.getElementById("saleStatus");
  const timerEl = document.getElementById("saleTimer");

  function updateCountdown() {
    const now = new Date();

    if (now < startDate) {
      // before sale
      statusEl.textContent = "Sale starts in:";
      const diff = startDate - now;
      timerEl.textContent = formatTime(diff);
    } else if (now >= startDate && now <= endDate) {
      // current sale
      statusEl.textContent = "Sale ends in:";
      const diff = endDate - now;
      timerEl.textContent = formatTime(diff);
    } else {
      // after sale
      statusEl.textContent = "Sale has ended";
      timerEl.textContent = "";
      clearInterval(interval);
    }
  }

  function formatTime(ms) {
    if (ms <= 0) return "0d 0h 0m 0s";

    const totalSeconds = Math.floor(ms / 1000);
    const days = Math.floor(totalSeconds / (3600 * 24));
    const hours = Math.floor((totalSeconds % (3600 * 24)) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    // add some zeros before single digits
    const pad = (n) => String(n).padStart(2, "0");
    return `${days}d ${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`;
  }

  updateCountdown();
  const interval = setInterval(updateCountdown, 1000);
});


const socialsContainer = document.getElementById("socialsContainer");
const socialsText = [
  '<a href="https://discord.gg/vzDV2ddt2V" target="_blank">Join Our Discord</a>',
  '<a href="https://www.tiktok.com/@frayyed.com" target="_blank">Follow Our Tiktok</a>',
  '<a href="https://www.instagram.com" target="_blank">Follow Our Instagram</a>',
];
let current = 0;
function switchSocialsText() {
    socialsContainer.style.opacity = 0;

  setTimeout(() =>{
    current = (current + 1) % socialsText.length
    socialsContainer.innerHTML = socialsText[current];
    socialsContainer.style.opacity = 1;
  }, 500);
}
  setInterval(switchSocialsText, 5000);