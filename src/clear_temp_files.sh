find . -name "#*#" | xargs -r rm
find . -name "*.pyc" | xargs -r rm
find . -name "*.retry" | xargs -r rm
find . -name "*~" | xargs -r rm;
