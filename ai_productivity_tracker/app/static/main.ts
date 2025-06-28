const text = "Your AI-powered productivity companion.";
const typedText = document.getElementById("typed-text")!;
let index = 0;

function typeNextChar() {
  if (index < text.length) {
    typedText.textContent += text.charAt(index);
    index++;
    setTimeout(typeNextChar, 50);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  typeNextChar();
});
