import * as sass from 'sass';

export default async function(eleventyConfig) {
    eleventyConfig.setInputDirectory('_templates');
    eleventyConfig.setLayoutsDirectory('_layouts');
    eleventyConfig.setOutputDirectory('_site');

    eleventyConfig.addTemplateFormats('scss');
    eleventyConfig.addExtension('scss', {
      outputFileExtension: 'css',
      compile: async function(inputContent) {
        let result = sass.compileString(inputContent);
        return async (data) => { return result.css };
      }
    });

    eleventyConfig.addTemplateFormats('js');
    eleventyConfig.addExtension('js', {
      outputFileExtension: 'js',
      compile: async function(inputContent) {
        return async (data) => { return inputContent; };
      }
    });

    eleventyConfig.addPassthroughCopy({ "crates/*/pkg/*.wasm": "wasm" });
    eleventyConfig.addPassthroughCopy({ "crates/*/pkg/*.js": "wasm" });

}
