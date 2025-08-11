// --- Configuration -----------------------------------------------------------
const CONFIG = {
  OWNER: "HasanBradfordUni",           // GitHub username
  REPO: "myPublicFiles",               // Repository name
  BRANCH: "main",                      // Branch GitHub Pages is publishing from
  CARDS_PATH: "cards",                 // Path to your folder containing card images
  CACHE_TTL_MS: 6 * 60 * 60 * 1000     // 6-hour cache timeout for API results
};

// Optional: force using GitHub API download_url for images (usually not needed)
// If false, images are loaded from your Pages site via relative paths (faster).
const USE_DOWNLOAD_URLS = false;

// --- Helpers: repo detection and API URL ------------------------------------
function detectRepoContext() {
  const host = window.location.hostname;
  const pathParts = window.location.pathname.split("/").filter(Boolean);
  const m = host.match(/^([^.]+)\.github\.io$/);
  const owner = CONFIG.OWNER || (m ? m[1] : null);
  // On project pages, first path segment is repo; on user/org pages it's absent.
  const repo = CONFIG.REPO || (m && pathParts.length ? pathParts[0] : null);
  const branch = CONFIG.BRANCH || "main";
  return { owner, repo, branch };
}

function ghContentsUrl(owner, repo, cardsPath, branch) {
  const encPath = encodeURIComponent(cardsPath).replace(/%2F/g, "/");
  const encRef = encodeURIComponent(branch);
  return `https://api.github.com/repos/${owner}/${repo}/contents/${encPath}?ref=${encRef}`;
}

// --- Storage cache -----------------------------------------------------------
function cacheKey({ owner, repo, branch }, path) {
  return `cards_manifest::${owner || "?"}::${repo || "?"}::${branch}::${path}`;
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
  } catch {
    // ignore quota errors
  }
}

function clearCache(key) {
  try { localStorage.removeItem(key); } catch {}
}

// --- Filename utilities ------------------------------------------------------
function baseName(path) {
  const f = path.split("/").pop();
  return f.replace(/\.[a-z0-9]+$/i, "");
}

function normalize(s) {
  return String(s)
    .toLowerCase()
    .replace(/[_-]+/g, " ")
    .replace(/[^a-z0-9 ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function titleCase(s) {
  return s
    .split(" ")
    .filter(Boolean)
    .map(w => w[0] ? w[0].toUpperCase() + w.slice(1) : w)
    .join(" ");
}

function isImageName(name) {
  return /\.(png|jpe?g|webp|gif|svg)$/i.test(name);
}

// --- Fetch folder listing from GitHub ---------------------------------------
async function fetchCardFilenames() {
  const ctx = detectRepoContext();
  const { owner, repo, branch } = ctx;

  const infoEl = document.getElementById("sourceInfo");
  if (!owner || !repo) {
    infoEl.textContent = "Set OWNER/REPO in app.js (auto-detect failed).";
  } else {
    infoEl.textContent = `${owner}/${repo}@${branch} • ${CONFIG.CARDS_PATH}`;
  }

  const cKey = cacheKey(ctx, CONFIG.CARDS_PATH);
  const cached = readCache(cKey, CONFIG.CACHE_TTL_MS);
  if (cached && cached.length) return cached;

  if (!owner || !repo) throw new Error("Missing owner or repo to query GitHub API.");

  const url = ghContentsUrl(owner, repo, CONFIG.CARDS_PATH, branch);
  const resp = await fetch(url, {
    headers: { "Accept": "application/vnd.github.v3+json" }
  });
  if (!resp.ok) {
    throw new Error(`GitHub API error ${resp.status}`);
  }
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
const IMG_BASE = "cards/"; // used when not using download_url
const imgEl = document.getElementById("cardImage");
const loadingEl = document.getElementById("loading");
const scoreEl = document.getElementById("score");
const formEl = document.getElementById("guessForm");
const inputEl = document.getElementById("guessInput");
const submitBtn = document.getElementById("submitBtn");
const feedbackEl = document.getElementById("feedback");
const nextBtn = document.getElementById("nextBtn");
const resetBtn = document.getElementById("resetBtn");

let ORDER = [];     // array of filenames or full URLs
let IDX = 0;
let ATTEMPTED = 0;  // completed cards
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
  // entry is either "filename.ext" or a full download_url
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
    if (!items.length) {
      throw new Error("No image files found in cards folder.");
    }

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
    feedbackEl.textContent = `Couldn't load cards automatically: ${err.message}. 
You can set OWNER/REPO/BRANCH in app.js or try again.`;
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
  const ctx = detectRepoContext();
  clearCache(cacheKey(ctx, CONFIG.CARDS_PATH));
  startGame();
});

// Enter key goes Next after answering
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && ANSWERED && !nextBtn.disabled) {
    e.preventDefault();
    nextBtn.click();
  }
});

// Boot
startGame();
