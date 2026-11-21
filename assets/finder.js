/* Board Game Finder — vanilla JS, no dependencies. Data is embedded in the page as window.GAMES. */
(function () {
  var form = document.getElementById("finder-form");
  var out = document.getElementById("finder-results");
  var count = document.getElementById("finder-count");
  if (!form || !out || !window.GAMES) return;

  function fmtPlayers(g) {
    if (g.playersMin == null) return "—";
    if (g.playersMax == null) return g.playersMin + "+ players";
    if (g.playersMin === g.playersMax) return g.playersMin + " players";
    return g.playersMin + "–" + g.playersMax + " players";
  }
  function fmtTime(g) {
    if (g.timeMin == null) return "—";
    if (g.timeMin === g.timeMax) return g.timeMin + " min";
    return g.timeMin + "–" + g.timeMax + " min";
  }
  function fmtPrice(g) {
    if (g.priceUSD == null) return "Price not verified — check Amazon / Target before you buy.";
    return "$" + g.priceUSD.toFixed(2) + " (checked 22 Nov 2026 — prices change, check the store before you buy).";
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function run() {
    var players = form.elements["players"].value; // any | 1 | 2 | 3-4 | 5+
    var time = form.elements["time"].value; // any | under30 | 30-60 | over60
    var budget = form.elements["budget"].value; // any | under30 | 30-60 | over60
    var type = form.elements["type"].value; // any | strategy | party | cooperative | family
    var includeUnknown = form.elements["includeUnknown"].checked;

    var results = window.GAMES.filter(function (g) {
      if (players !== "any") {
        if (players === "1" && !(g.playersMin <= 1)) return false;
        if (players === "2" && !(g.playersMin <= 2 && (g.playersMax == null || g.playersMax >= 2))) return false;
        if (players === "3-4" && !(g.playersMin <= 4 && (g.playersMax == null || g.playersMax >= 3))) return false;
        if (players === "5+" && !(g.playersMax == null || g.playersMax >= 5)) return false;
      }
      if (time !== "any") {
        if (g.timeMin == null) return false;
        if (time === "under30" && !(g.timeMax <= 30)) return false;
        if (time === "30-60" && !(g.timeMin <= 60 && g.timeMax >= 30)) return false;
        if (time === "over60" && !(g.timeMax > 60)) return false;
      }
      if (type !== "any" && g.type !== type) return false;
      if (budget !== "any") {
        if (g.priceUSD == null) return includeUnknown;
        if (budget === "under30" && !(g.priceUSD < 30)) return false;
        if (budget === "30-60" && !(g.priceUSD >= 30 && g.priceUSD <= 60)) return false;
        if (budget === "over60" && !(g.priceUSD > 60)) return false;
      }
      return true;
    });

    count.textContent = results.length + (results.length === 1 ? " game found" : " games found");
    if (!results.length) {
      out.innerHTML = "<p>No games in our list match all of those filters. Try widening the time or budget — or start with the <a href=\"/gamenightguide/guides/best-board-games-for-beginners/\">beginners guide</a>.</p>";
      return;
    }
    out.innerHTML = results.map(function (g) {
      var bits = [fmtPlayers(g), fmtTime(g)];
      if (g.ageMin != null) bits.push("Ages " + g.ageMin + "+");
      if (g.bgg != null) bits.push("BGG " + g.bgg + "/10");
      return '<div class="finder-result"><h3>' + esc(g.name) + '</h3>' +
        "<p><strong>" + bits.join(" · ") + "</strong></p>" +
        "<p>" + esc(g.bestFor) + "</p>" +
        "<p class=\"muted\">" + fmtPrice(g) + "</p></div>";
    }).join("");
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
  form.addEventListener("change", run);
  run();
})();
