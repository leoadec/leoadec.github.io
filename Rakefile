require "html-proofer"
require "jekyll"

task :build do
  Jekyll::Site.new(Jekyll.configuration()).process
end

task :test do
  HTMLProofer.check_directory("./_site").run
end

task serve:[:build] do
  sh "bundle exec jekyll serve";
end

task :clean do
  sh "rm -rf _site";
end
