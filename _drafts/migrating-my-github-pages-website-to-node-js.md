---
---
As many other people, I have been using GitHub Pages to host my personal
website: it is free, comes with unlimited CI/CD, and is quite straightforward.

It is also powered behind the scenes by Jekyll, a static site generator built in
Ruby, which is a language I don't have that much familiarity with, and whose
adoption has been dwindling over the years. I had some aspirations to make the
website more complex, and for these I would probably need tools outside the Ruby
sphere, tools likely built with Node.js. In which case, why not build the
website in Node.js itself?

## Preparations

The first thing to notice is that you can customize the CI/CD for GitHub pages
deployment. In that way, if you have a `"script"` field specified in your
`packages.json`, you can add the commands there that test and build your
website.
