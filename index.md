---
title: Curriculum Vit&aelig;
layout: default
---

<h3>Professional experience</h3>
<ul>
{% assign jobs = site.jobs | reverse %}
{% for job in jobs %}
  <li seq="{{ job.date | date: '%Y' }}&ndash;{% if job.end_date %}{{ job.end_date | date: '%Y' }}{% else %}current{% endif %}">
    <strong>{{ job.title }}.</strong>
    {{ job.employer }} ({{ job.location }})
    <!--<div class="details">
      {{ job.content | markdownify }}
    </div>-->
  </li>
{% endfor %}
</ul>

<h3>Education</h3>
<ul>
{% assign degrees = site.degrees | reverse %}
{% for degree in degrees %}
  <li seq="{{ degree.date | date: '%Y' }}&ndash;{% if degree.end_date %}{{ degree.end_date | date: '%Y' }}{% else %}current{% endif %}">
    <strong>{{ degree.title }}.</strong>
    {{ degree.employer }} ({{ degree.location }})
    <!--<div class="details">
      {{ degree.content | markdownify }}
    </div>-->
  </li>
{% endfor %}
</ul>

<h3>Papers published</h3>
<ul>
{% for post in site.posts %}
{% include papers.html papers=post.papers %}
{% endfor %}
</ul>

<h3>Conference talks</h3>
<ul>
{% for post in site.posts %}
{% include talks.html talks=post.conference_talks %}
{% endfor %}
</ul>

<h3>Conference posters</h3>
<ul>
{% for post in site.posts %}
{% include posters.html posters=post.conference_posters %}
{% endfor %}
</ul>

<h3>Volunteer work</h3>
<ul>
{% for post in site.posts %}
{% include work.html works=post.volunteer_work %}
{% endfor %}
</ul>

<h3>Grants</h3>
<ul>
{% assign grants = site.grants | reverse %}
{% for grant in grants %}
   <li seq="{{ grant.date | date: '%Y' }}&ndash;{% if grant.end_date %}{{ grant.end_date | date: '%Y' }}{% else %}current{% endif %}">
     <strong>{{ grant.title }}</strong>. {{ grant.agency }}. <br/>
     <a href="{{ grant.external_url }}" class="title">{{ grant.project }}.</a>
   </li>
{% endfor %}
</ul>
