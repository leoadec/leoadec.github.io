require "html-proofer"
require "jekyll"

task :build do
  Jekyll::Site.new(Jekyll.configuration()).process
end

task test:[:build] do
  options = {
    ignore_urls: [
      /bv.fapesp.br/, /linkedin.com/, /physics.sk/, /sciencedirect.com/
    ]
  }
  HTMLProofer.check_directory("./_site", options).run
end

task serve:[:build] do
  sh "bundle exec jekyll serve";
end

task serve_dev:[:build] do
  sh "bundle exec jekyll serve --unpublished";
end

task :clean do
  sh "rm -rf _site";
end
