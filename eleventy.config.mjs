import mathjax from 'mathjax';
import * as sass from 'sass';

const MathJax = await mathjax.init({
    loader: { load: ['input/tex', 'output/svg'] },
})

export default async function(eleventyConfig) {
    eleventyConfig.setInputDirectory('_templates');
    eleventyConfig.setLayoutsDirectory('_layouts');
    eleventyConfig.setOutputDirectory('_site');

    eleventyConfig.addTemplateFormats('mathjax');
    eleventyConfig.addExtension('mathjax', {
      outputFileExtension: 'svg',
      compile: async function(inputContent) {
        let result = MathJax.tex2svg(inputContent);
        return async (data) => { return MathJax.startup.adaptor.innerHTML(result) };
      }
    });

    eleventyConfig.addTemplateFormats('scss');
    eleventyConfig.addExtension('scss', {
      outputFileExtension: 'css',
      compile: async function(inputContent) {
        let result = sass.compileString(inputContent);
        return async (data) => { return result.css };
      }
    });
}
