---
layout: layouts/base.njk
title: Game Night Guide
description: "Board games for beginners, couples and families, in plain English. What to buy first, what plays well with two people, and what works for a family game night."
image: /images/og-home.jpg
imageAlt: "Friends playing a board game at a wooden table, Game Night Guide"
---

<div class="home-hero">
  <img src="/images/photos/hero-home.jpg" alt="Friends playing a board game at a wooden table on a warm evening" width="1600" height="900" loading="eager">
  <div class="home-hero-text">
    <h1>Board games, in plain English.</h1>
    <p class="lede">Buy one game tonight. Play it tonight. We tell you how many players it needs, how long it takes, what age it suits, and what it costs.</p>
    <p><a class="btn" href="/finder/">Find your game</a> <a class="btn-ghost" href="/guides/best-board-games-for-beginners/">Start with beginners</a></p>
  </div>
</div>

## Start here: who is playing?

<div class="card-grid three">
  <div class="card">
    <img src="/images/photos/beginners-thumb.jpg" alt="Friends laughing over a board game at a wooden table" width="600" height="375" loading="lazy">
    <p class="tag">First game</p>
    <h3><a href="/guides/best-board-games-for-beginners/">Beginners</a></h3>
    <p>Never played a modern board game? Ten easy games, all learnable in about ten minutes.</p>
  </div>
  <div class="card">
    <img src="/images/photos/couples-thumb.jpg" alt="A young couple playing chess together at home" width="600" height="375" loading="lazy">
    <p class="tag">Date night</p>
    <h3><a href="/guides/best-board-games-for-couples/">Couples</a></h3>
    <p>Games made for two, not games that just allow two. Patchwork, Jaipur and 7 Wonders Duel lead the list.</p>
  </div>
  <div class="card">
    <img src="/images/photos/2-players-under-40-thumb.jpg" alt="Friends playing a board game seen from above" width="600" height="375" loading="lazy">
    <p class="tag">Two players</p>
    <h3><a href="/guides/best-board-games-for-2-players-under-40/">2 players under $40</a></h3>
    <p>Two-player games that are actually good with two, at a price you can plan around.</p>
  </div>
</div>

<div class="callout">
  <h2>Find your game in 30 seconds</h2>
  <p>Answer four questions: players, time, budget, type. The Finder narrows our list to the games that fit your table.</p>
  <p><a class="btn" href="/finder/">Try the Board Game Finder</a></p>
</div>

## How to choose your first game

1. **Count the players.** Most game nights are 2 people, or 3 to 4. A game that says "2 to 5 players" is not always good with 2.
2. **Check the time.** A 30-minute game gets played. A 3-hour game sits on the shelf. Start under 60 minutes.
3. **Learn the rules in 10 minutes.** The best first games, Ticket to Ride, Codenames, Azul, Carcassonne, Sushi Go!, are teachable in under ten minutes and finish in under an hour.
4. **Buy one, not five.** One good gateway game beats a shelf of games nobody has learned yet.

## How we pick games

We only recommend games we can describe with facts: players, time, age, and a BoardGameGeek rating where one exists. We publish a price only when we have verified it, and we date-stamp every check. Where a price is not verified, we say so, in the guide itself.

Game facts were last checked 22 Nov 2026. Prices change often, so always check the live price at the store before you buy.

## All guides

<div class="card-grid">
{% for post in collections.guides %}
  <div class="card">
    {% if post.data.photo %}<img src="{{ post.data.photo | replace('.jpg', '-thumb.jpg') }}" alt="{{ post.data.imageAlt or post.data.title }}" width="600" height="375" loading="lazy">{% endif %}
    <h3><a href="{{ post.url }}">{{ post.data.title }}</a></h3>
    <p>{{ post.data.description }}</p>
    <p class="muted">{{ post.date | readableDate }} · Last checked {{ site.lastChecked }}</p>
  </div>
{% endfor %}
</div>

## A note on prices and facts

Board game prices change often, and a game's price at Amazon is not the same as at Target. We only publish a price when we have verified it, and we date-stamp every check. Where a price is not verified, we say so.

See the note at the top of each guide. Game facts (players, time, age, BoardGameGeek rating) were last checked 22 Nov 2026.
