task :build do
  sh "bundle exec jekyll build --destination _site";
end

task serve:[:build] do
  sh "bundle exec jekyll serve";
end

task :clean do
  sh "rm -rf _site";
end
