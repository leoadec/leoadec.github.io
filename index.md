---
layout: default
---

Quantum devices have the potential to revolutionize many areas of technology,
from computers to sensors. I work with the development of software that enables
quantum technology to become more efficient and realize its potential sooner.

---

## Professional experience
<ul>
{% assign jobs = site.jobs | reverse %}
{% for job in jobs %}
  <li seq="{% include year_range.html date=job.date end_date=job.end_date -%}">
    <strong>{{ job.title }}</strong> <br>
    {{ job.employer }} ({{ job.location }}).
    <div class="details">
      {{ job.content }}
    </div>
  </li>
{% endfor %}
</ul>

## Education
<ul>
{% assign degrees = site.degrees | reverse %}
{% for degree in degrees %}
  <li seq="{% include year_range.html date=degree.date end_date=degree.end_date -%}">
    <strong>{{ degree.title }}</strong> <br>
    {{ degree.university }} ({{ degree.location }}).
    {% if degree.grant %} <br/>
     Grant: {{ degree.grant.agency }}. <a href="{{ degree.grant.external_url }}" class="title">{{ degree.grant.project }}</a>.
     ({% include year_range.html date=degree.grant.date end_date=degree.grant.end_date -%})
    {% endif %}
    <div class="details">
      {{ degree.content | markdownify }}
    </div>
  </li>
{% endfor %}
</ul>

## Papers published
<ul>
{% assign papers = site.papers | reverse  %}
{% for paper in papers limit:12 %}
  <li>
  {% for author in paper.authors %}{{ author }}{% if forloop.last == false %}, {% endif %}{% endfor %}.
  &quot;<a href="{{ paper.external_url }}" target="_blank">{{ paper.title }}{% if paper.subtitle %}: {{ paper.subtitle }}{% endif %}</a>&quot;.
  {{ paper.journal }} <span class="volume">{{ paper.volume }}</span>, {{ paper.pages }} ({{ paper.date | date: '%Y' }}).
  {% if paper.doi %}<a href="https://dx.doi.org/{{ paper.doi }}" target="_blank">[DOI:{{ paper.doi }}]</a>{% endif %}
  <a href="https://arxiv.org/abs/{{ paper.arxiv }}" target="_blank">[arXiv:{{ paper.arXiv }}]</a>
  </li>
{% endfor %}
</ul>

## Conference talks
<ul>
{% assign conferences = site.conferences | reverse %}
{% for conference in conferences limit:5 %}
  {{ conference }}
  {% if conference.talk %}
  <li>
  {% for author in conference.talk_authors %}{{ author }}{% if forloop.last == false %}, {% endif %}{% endfor %}.
  &quot;{{ conference.talk }}&quot;.
  {{ conference.name }} {{ conference.date | date: '%Y' }} ({{ conference.location }}).
  </li>
  {% endif %}
{% endfor %}
</ul>

## Conference posters
<ul>
{% for conference in conferences limit:5 %}
  {% if conference.poster %}
  <li>
  {% for author in conference.poster_authors %}{{ author }}{% if forloop.last == false %}, {% endif %}{% endfor %}.
  &quot;{{ conference.poster }}&quot;.
  {{ conference.name }} {{ conference.date | date: '%Y' }} ({{ conference.location }}).
  </li>
  {% endif %}
{% endfor %}
</ul>
