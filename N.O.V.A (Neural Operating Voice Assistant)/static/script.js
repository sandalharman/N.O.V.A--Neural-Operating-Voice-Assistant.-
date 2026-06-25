const chatWindow = document.getElementById("chatWindow");
const cmdInput = document.getElementById("cmd");

let lastHistoryLength = -1;

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderHistory(history) {
  if (!Array.isArray(history)) return;
  if (history.length === lastHistoryLength) return;
  lastHistoryLength = history.length;

  chatWindow.innerHTML = history.map(item => {
    const role = item.role === "user" ? "user" : "assistant";
    const title = role === "user" ? "You" : "NOVA";
    return `
      <div class="message ${role}">
        <span class="role">${title}</span>
        ${escapeHtml(item.text)}
      </div>
    `;
  }).join("");

  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function updateState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  document.getElementById("status").textContent = data.status;
  document.getElementById("orbStatus").textContent = String(data.status).toUpperCase();
  renderHistory(data.history);
}

async function listen() {
  await fetch("/api/listen", { method: "POST" });
  setTimeout(updateState, 700);
}

async function sendCommand() {
  const text = cmdInput.value.trim();
  if (!text) return;

  cmdInput.value = "";
  autoResize();

  const res = await fetch("/api/command", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });

  const data = await res.json();
  renderHistory(data.history);
  updateState();
}

function quick(text) {
  cmdInput.value = text;
  sendCommand();
}

function clearChat() {
  chatWindow.innerHTML = "";
  lastHistoryLength = -1;
}

function autoResize() {
  cmdInput.style.height = "46px";
  cmdInput.style.height = Math.min(cmdInput.scrollHeight, 150) + "px";
}

cmdInput.addEventListener("input", autoResize);

cmdInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendCommand();
  }
});

setInterval(updateState, 1200);
updateState();
