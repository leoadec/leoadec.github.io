---
title: Curriculum Vit&aelig;
layout: default
---

<h3>Professional experience</h3>
<ul>
{% for post in site.posts %}
  {% if post.tag == "career" %}
   <li seq="{{ post.date | date: '%Y' }}&ndash;{% if post.end_date %}{{ post.end_date | date: '%Y' }}{% else %}current{% endif %}">
     <strong>{{ post.title }}.</strong>
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

<h3>Education</h3>
<ul>
{% for post in site.degrees %}
   <li seq="{{ post.date | date: '%Y' }}&ndash;{% if post.end_date %}{{ post.end_date | date: '%Y' }}{% else %}current{% endif %}">
     <strong>{{ post.title }}.</strong>
     {{ post.employer }} ({{ post.location }})
     <div class="details">
       {{ post.content | markdownify }}
     </div>
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
{% for post in site.posts %}
{% include grants.html grants=post.grants %}
{% endfor %}
</ul>
