---
layout: layouts/base.njk
title: All Guides
description: "Every board game guide on Game Night Guide: beginners, couples, 2 players, solo play, and head-to-head comparisons."
permalink: /guides/index.html
---

<h1>All guides</h1>

<p class="lede">Every guide lists players, time, age and price, and says plainly when a price has not been verified.</p>

{% for post in collections.guides %}
<div class="card">
  <h3><a href="{{ post.url }}">{{ post.data.title }}</a></h3>
  <p>{{ post.data.description }}</p>
  <p class="muted">{{ post.date | readableDate }} · Last checked {{ site.lastChecked }}</p>
</div>
{% endfor %}
