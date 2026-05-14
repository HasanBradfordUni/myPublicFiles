async function getPlayerPrice() {
  const name = document.getElementById("player-name").value.trim();
  const platform = document.getElementById("platform").value;
  const resultsDiv = document.getElementById("results");

  if (!name) {
    resultsDiv.innerHTML = "<p style='color:red;'>Please enter a player name.</p>";
    return;
  }

  resultsDiv.innerHTML = "<p>Loading...</p>";

  try {
    const response = await fetch(`/api/player?name=${encodeURIComponent(name)}&platform=${platform}`);
    const data = await response.json();

    if (data.error) {
      resultsDiv.innerHTML = `<p style='color:red;'>${data.error}</p>`;
      return;
    }

    resultsDiv.innerHTML = `
      <h2>${name.toUpperCase()}</h2>
      <p><strong>Platform:</strong> ${data.platform}</p>
      <p><strong>Price:</strong> ${data.price} coins</p>
      <p><strong>Last Updated:</strong> ${data.updated}</p>
      <p><small>Player ID: ${data.player_id}</small></p>
    `;
  } catch (err) {
    resultsDiv.innerHTML = `<p style='color:red;'>Error: ${err.message}</p>`;
  }
}
