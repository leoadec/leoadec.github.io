require "jekyll"

task :build do
  Jekyll::Site.new(Jekyll.configuration()).process
end

task serve:[:build] do
  sh "bundle exec jekyll serve";
end

task :clean do
  sh "rm -rf _site";
end
