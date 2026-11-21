---
layout: layouts/base.njk
title: Board Game Finder
description: Answer four questions — players, time, budget, type — and find a board game that fits your table. Free, no sign-up, works offline.
image: /images/og-finder.png
imageAlt: Board Game Finder — find your next board game
permalink: /finder/index.html
---

<h1>Board Game Finder</h1>

<p class="lede">Four questions, one short list. The Finder only uses games from our own list — the games we have written about and checked.</p>

<form id="finder-form">
  <label for="f-players">How many players?</label>
  <select id="f-players" name="players">
    <option value="any">Any</option>
    <option value="1">Just me (solo)</option>
    <option value="2">2 players</option>
    <option value="3-4">3–4 players</option>
    <option value="5+">5 or more players</option>
  </select>

  <label for="f-time">How much time?</label>
  <select id="f-time" name="time">
    <option value="any">Any</option>
    <option value="under30">Under 30 minutes</option>
    <option value="30-60">30–60 minutes</option>
    <option value="over60">Over 60 minutes</option>
  </select>

  <label for="f-budget">Budget</label>
  <select id="f-budget" name="budget">
    <option value="any">Any budget</option>
    <option value="under30">Under $30</option>
    <option value="30-60">$30–$60</option>
    <option value="over60">Over $60</option>
  </select>

  <label for="f-type">What kind of game?</label>
  <select id="f-type" name="type">
    <option value="any">Any type</option>
    <option value="strategy">Strategy</option>
    <option value="party">Party</option>
    <option value="cooperative">Cooperative</option>
    <option value="family">Family</option>
  </select>

  <label><input type="checkbox" name="includeUnknown" checked> Include games whose price we have not verified</label>

  <button type="submit">Find my game</button>
</form>

<p id="finder-count" aria-live="polite"></p>
<div id="finder-results" aria-live="polite"></div>

<script>
window.GAMES = {{ games | dump | safe }};
</script>
<script src="/assets/finder.js"></script>

## How the Finder works

- **Players:** a game matches if your group size is inside its player range. A game listed as “2–5 players” matches 2, 3–4 and 5+.
- **Budget:** we only filter on prices we have actually verified (checked 22 Nov 2026). Most games in our list have no verified price yet, so they only appear when “Include games whose price we have not verified” is ticked — or when you pick “Any budget”. Prices change; always check the live price at the store before you buy.
- **No tracking:** the Finder runs entirely in your browser. Nothing you pick is sent anywhere.

Not sure where to start? Read the [beginners guide](/guides/best-board-games-for-beginners/) first.
