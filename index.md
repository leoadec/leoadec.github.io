---
layout: index
title: About
lang: en
---

Quantum technology will unleash many new possibilities in the coming years,
from more sensitive sensors to computers capable of results that none of the
conventional ones can.
I became interested in this field during my undergraduate studies in physics,
and continued studying the theory of how to make quantum tech possible through
three degrees and two jobs across three countries.
Currently I am part of the quantum industry, leading a team of engineers who
develop software to extract the maximum performance from quantum tech devices.

[Full CV](cv.html)

<div class="snippet">
<h3>Professional experience</h3>
<ul>
{% for post in site.posts %}
  {% if post.tag == "career" %}
   <li seq="{{ post.date | date: '%Y' }}&ndash;{% if post.end_date %}{{ post.end_date | date: '%Y' }}{% else %}current{% endif %}">
     <strong>{{ post.title }}</strong>.
     {{ post.employer }} ({{ post.location }})
     {% if post.bullet_points %}
     <ul class="details">
       {% for point in post.bullet_points %}
       <li>{{ point }}</li>
       {% endfor %}
     </ul>
     {% endif %}
   </li>
  {% endif %}
{% endfor %}
</ul>
</div>

<div class="snippet">
<h3>Education</h3>
<ul>
{% for post in site.posts %}
  {% if post.tag == "education" %}
   <li seq="{{ post.date | date: '%Y' }}&ndash;{% if post.end_date %}{{ post.end_date | date: '%Y' }}{% else %}current{% endif %}">
     <strong>{{ post.title }}</strong>.
     {{ post.university }} ({{ post.location }})
     {% if post.bullet_points %}
     <ul class="details">
       {% for point in post.bullet_points %}
       <li>{{ point }}</li>
       {% endfor %}
     </ul>
     {% endif %}
   </li>
  {% endif %}
{% endfor %}
</ul>
</div>
