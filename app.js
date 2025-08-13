// --- Configuration -----------------------------------------------------------
const CONFIG = {
  OWNER: "HasanBradfordUni",
  REPO: "myPublicFiles",
  BRANCH: "main",
  CARDS_PATH: "cards",
  CACHE_TTL_MS: 6 * 60 * 60 * 1000
};

const USE_DOWNLOAD_URLS = false;

// --- Helpers -----------------------------------------------------------------
function ghContentsUrl(owner, repo, cardsPath, branch) {
  const encPath = encodeURIComponent(cardsPath).replace(/%2F/g, "/");
  const encRef = encodeURIComponent(branch);
  return `https://api.github.com/repos/${owner}/${repo}/contents/${encPath}?ref=${encRef}`;
}

function cacheKey(path) {
  return `cards_manifest::${CONFIG.OWNER}::${CONFIG.REPO}::${CONFIG.BRANCH}::${path}`;
}

function readCache(key, ttlMs) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const { ts, items } = JSON.parse(raw);
    if (!ts || !Array.isArray(items)) return null;
    if (Date.now() - ts > ttlMs) return null;
    return items;
  } catch {
    return null;
  }
}

function writeCache(key, items) {
  try {
    localStorage.setItem(key, JSON.stringify({ ts: Date.now(), items }));
  } catch {}
}

function clearCache(key) {
  try { localStorage.removeItem(key); } catch {}
}

function baseName(path) {
  const f = path.split("/").pop();
  return f.replace(/\.[a-z0-9]+$/i, "");
}

function normalize(s) {
  return String(s).toLowerCase().replace(/[_-]+/g, " ").replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
}

function titleCase(s) {
  return s.split(" ").filter(Boolean).map(w => w[0] ? w[0].toUpperCase() + w.slice(1) : w).join(" ");
}

function isImageName(name) {
  return /\.(png|jpe?g|webp|gif|svg)$/i.test(name);
}

// --- Fetch folder listing from GitHub ---------------------------------------
async function fetchCardFilenames() {
  const infoEl = document.getElementById("info");
  infoEl.textContent = `${CONFIG.OWNER}/${CONFIG.REPO}@${CONFIG.BRANCH} • ${CONFIG.CARDS_PATH}`;

  const cKey = cacheKey(CONFIG.CARDS_PATH);
  const cached = readCache(cKey, CONFIG.CACHE_TTL_MS);
  if (cached && cached.length) return cached;

  const url = ghContentsUrl(CONFIG.OWNER, CONFIG.REPO, CONFIG.CARDS_PATH, CONFIG.BRANCH);
  const resp = await fetch(url, {
    headers: { "Accept": "application/vnd.github.v3+json" }
  });
  if (!resp.ok) throw new Error(`GitHub API error ${resp.status}`);
  const json = await resp.json();
  if (!Array.isArray(json)) throw new Error("Unexpected API response.");

  const files = json
    .filter(item => item && item.type === "file" && isImageName(item.name))
    .map(item => ({
      name: item.name,
      download_url: item.download_url
    }));

  const names = files.map(f => f.name);
  writeCache(cKey, USE_DOWNLOAD_URLS ? files.map(f => f.download_url) : names);
  return USE_DOWNLOAD_URLS ? files.map(f => f.download_url) : names;
}

// --- UI/Quiz logic -----------------------------------------------------------
const IMG_BASE = "cards/";
const imgEl = document.getElementById("cardImage");
const loadingEl = document.getElementById("loading");
const scoreEl = document.getElementById("score");
const formEl = document.getElementById("guessForm");
const inputEl = document.getElementById("guessInput");
const submitBtn = document.getElementById("submitBtn");
const feedbackEl = document.getElementById("feedback");
const nextBtn = document.getElementById("nextBtn");
const resetBtn = document.getElementById("resetBtn");

let ORDER = [];
let IDX = 0;
let ATTEMPTED = 0;
let CORRECT = 0;
let ANSWERED = false;
let LAST_OK = false;

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function updateScore() {
  scoreEl.textContent = `Score: ${CORRECT}/${ATTEMPTED}`;
}

function clearFeedback() {
  feedbackEl.className = "feedback";
  feedbackEl.textContent = "";
}

function showFeedback(isCorrect, expected) {
  feedbackEl.className = `feedback show ${isCorrect ? "ok" : "nope"}`;
  feedbackEl.textContent = isCorrect
    ? `Correct! It's ${titleCase(expected)}.`
    : `Not quite. Correct answer: ${titleCase(expected)}.`;
}

function currentDisplayName(entry) {
  const name = entry.includes("://")
    ? entry.split("/").pop().split("?")[0]
    : entry;
  return baseName(name);
}

function loadCurrentCard() {
  const entry = ORDER[IDX];
  if (!entry) return;
  imgEl.src = entry.includes("://") ? entry : (IMG_BASE + entry);
  imgEl.alt = "FIFA card type to guess";
}

async function startGame() {
  try {
    loadingEl.style.display = "grid";
    submitBtn.disabled = true;
    nextBtn.disabled = true;
    inputEl.disabled = true;

    const items = await fetchCardFilenames();
    if (!items.length) throw new Error("No image files found in cards folder.");

    ORDER = shuffle(items);
    IDX = 0; ATTEMPTED = 0; CORRECT = 0; ANSWERED = false; LAST_OK = false;
    updateScore();
    loadCurrentCard();
    clearFeedback();

    inputEl.value = "";
    inputEl.disabled = false;
    submitBtn.disabled = false;
    loadingEl.style.display = "none";
    inputEl.focus();
  } catch (err) {
    loadingEl.style.display = "none";
    clearFeedback();
    feedbackEl.className = "feedback show nope";
    feedbackEl.textContent = `Couldn't load cards automatically: ${err.message}.`;
    console.error(err);
  }
}

function goNext() {
  ATTEMPTED += 1;
  if (LAST_OK) CORRECT += 1;
  updateScore();

  IDX += 1;
  if (IDX >= ORDER.length) {
    ORDER = shuffle(ORDER);
    IDX = 0;
  }
  loadCurrentCard();

  ANSWERED = false;
  LAST_OK = false;
  inputEl.value = "";
  inputEl.disabled = false;
  submitBtn.disabled = false;
  nextBtn.disabled = true;
  clearFeedback();
  inputEl.focus();
}

// Events
formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  if (ANSWERED) return;

  const entry = ORDER[IDX];
  const expected = normalize(currentDisplayName(entry));
  const guess = normalize(inputEl.value);

  LAST_OK = guess.length > 0 && guess === expected;
  ANSWERED = true;

  showFeedback(LAST_OK, expected);
  inputEl.disabled = true;
  submitBtn.disabled = true;
  nextBtn.disabled = false;
  nextBtn.focus();
});

nextBtn.addEventListener("click", () => {
  if (!ANSWERED) return;
  goNext();
});

resetBtn.addEventListener("click", () => {
  clearCache(cacheKey(CONFIG.CARDS_PATH));
  startGame();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && ANSWERED && !nextBtn.disabled) {
    e.preventDefault();
    nextBtn.click();
  }
});

startGame();
