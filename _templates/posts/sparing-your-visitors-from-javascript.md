---
title: Sparing your visitors from JavaScript
tagline: Building a static website in GitHub Pages with Eleventy
date: git Created
tags:
 - tech
 - JavaScript
layout: post.liquid
author: Leonardo Andreta de Castro
author_link: /
---

When creating my personal websites, I try to keep them as lightweight as
possible on the user side, to give visitors a fast-loading experience without
any hidden bloat running in their browsers. Although this usually means making
static websites without any scripts, I can't deny that much of the power of the
web resides on the many open-source JavaScript packages that exist today. So,
what if I ran them all on the server side before deploying my pages, serving to
the user just script-free static output?

I have hosted my personal website on
[GitHub Pages](https://docs.github.com/en/pages) for a few years, and it has
been a good tool for delivering static pages. It's a free service, it doesn't
add any bloat, and it's very flexible. It lets you use any tool that runs on a
public GitHub Actions workflow to generate your static website.

By default, GitHub Pages uses [Jekyll](https://jekyllrb.com), which is a good
Ruby package for making static pages. But if you want to customize your pipeline
to do more, it would be convenient to have a tool that integrates directly with
the JavaScript ecosystem that includes so many of the packages that simplify the
process of creating webpages.

For a while I had been considering migrating the website to some of the popular
frameworks like [React](https://react.dev) or [Next.js](https://nextjs.org),
but these were too bloated for my purposes. The resulting pages would require
embedded scripts, something that was unnecessary for my mostly unchanging
content.

I was close to giving up when I heard by accident of
[Eleventy](https://11ty.dev), which turned out to be the JavaScript-based
solution that was flexible and simple enough to replace Jekyll as my static
website generator on GitHub Pages.

## Setting it up

In general, Eleventy is very similar to Jekyll. You can create your
[LiquidJS](https://liquidjs.com) templates, pass data to them via Markdown
files, and Eleventy will output all the HTML pages for your website. If you
don't include JavaScript in your templates, the final output page won't have any
JavaScript, even though it was created with a JavaScript program.

Migrating is straightforward. If you have [Node.js](https://nodejs.org) set up,
you can install Eleventy in your GitHub Pages repository with:

```shell
npm install @11ty/eleventy
```

Adding these additional lines to your `packages.json` will allow you to have
similar functionality to `jekyll build` and `jekyll serve` with `npm run build`
and `npm run serve`:

```json
  "scripts": {
    "build": "npx @11ty/eleventy",
    "serve": "npx @11ty/eleventy --serve"
  }
```

Now you can run `npm run serve` and go to `http://localhost:8080` in your
browser to see a preview of your website generated from the Markdown files in 
your `_templates/` directory.

## Adding common functionality

Migrating from Jekyll to Eleventy wouldn't be worth the trouble if you just
wanted to convert Markdown to HTML. Let's take a look at what we can leverage
from the pool of open-source JavaScript packages to make the website generation
more interesting.

To start with a simple example, you might be used to converting
[Sass](https://sass-lang.com) files into CSS with Jekyll. To do the same with
Eleventy, you don't need to import a plugin, you can install the `sass` package
itself with `npm`:

```shell
npm install sass
```

Then, add some lines of code to the `eleventy.config.mjs` file to indicate that
whenever Eleventy encounters a `.scss` file, it should use the `sass` package to
compile it into a `.css` file:

```js
import * as sass from 'sass';

export default async function(eleventyConfig) {
  eleventyConfig.addTemplateFormats('scss');
  eleventyConfig.addExtension('scss', {
    outputFileExtension: 'css',
    compile: async function(inputContent) {
      let result = sass.compileString(inputContent);
      return async (data) => { return result.css };
    }
  });
}
```

With this, whenever you add `.scss` files to your `_templates/` directory, you
will see the `.css` files being populated in your website next time you run
`npm run build` or `npm run serve`.

The fact that you can include new packages into your pipeline without writing
much code opens up as many possibilities as the number of JavaScript packages
that exist out there. Let's take a look at an example that illustrates a need
that is not as common as compiling Sass files.

## Adding custom functionality

Imagine you want to include equations in your pages. You could use the popular
JavaScript package [MathJax](https://mathjax.org) for it, but loading it on the
user's browser to replace TeX code dynamically would add bloat to your pages.
(And, in my experience, also not work from time to time.)

Instead, you can install MathJax on the server side only, and give the user the
already rendered vector images with the equations. To do this, start by
installing it with `npm`:

```shell
npm install mathjax@3
```

Then, add some configuration lines to your `eleventy.config.mjs`:

```js
import mathjax from 'mathjax';

const MathJax = await mathjax.init({
  loader: { load: ['input/tex', 'output/svg'] },
});

export default async function(eleventyConfig) {
  // ...

  eleventyConfig.addTemplateFormats('mathjax');
  eleventyConfig.addExtension('mathjax', {
    outputFileExtension: 'svg',
    compile: async function(inputContent) {
      let result = MathJax.tex2svg(inputContent);
      return async (data) => {
        return MathJax.startup.adaptor.innerHTML(result)
      };
    }                                                                          
  });
}
```

This will convert any TeX files with the extension `.mathjax` in your 
`_templates/` directory into SVG figures. For example, if you write a TeX file
like this:

```latex
\oint_{\partial \Sigma} \mathbf{E} \cdot \mathrm{d} \ell =
- \frac{\mathrm{d}}{\mathrm{d} t} \int \int_{\Sigma} \mathbf{B}
\cdot \mathrm{d} \mathbf{S}.
```

It will be converted into a figure like this next time you run `npm run build`
or `npm run serve`:

![One of Maxwell's equations.](/assets/example.svg)

You can then refer to the SVG in your Markdown templates to load it from the
rendered page.

## Setting up continuous deployment for GitHub Pages

After you have installed all the modules you want to use in your pipeline, the
final step will be to adapt the GitHub Actions workflow to build the website
using Node.js and Eleventy instead of Jekyll. To do that, you will need to
enable
[publishing to GitHub Pages with a custom workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow).
If that is set up, you should be able to see a YAML file containing the
deployment workflow within your `.github/workflows/` folder.

Within the workflow YAML file, you just need to add a few build steps between
the `checkout` action and the `upload-pages-artifact`:

```yaml
  - name: Set up Node.js
    uses: actions/setup-node@v4
    with:
      node-version: 22
      cache: 'npm'
  - name: Install dependencies
    run: npm install
  - name: Build with Eleventy
    run: npm run build
```

You might also want to either update the `path` of `upload-pages-artifact` to
match the directory where Eleventy is outputting the static pages it generates,
or update `eleventy.config.mjs` so the output directory matches Jekyll's
default location (`_site`):

```js
  eleventyConfig.setOutputDirectory('_site');
```

With this, you should be good to go. Next time you merge changes to your GitHub
Pages repository your website will be built and deployed with Eleventy. And next
time you feel the need to load JavaScript modules on your website to support new
functionality, you might be able to do it on the server side instead.
