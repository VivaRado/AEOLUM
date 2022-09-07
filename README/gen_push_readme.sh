#!/bin/bash
commit_message="$1"

python3 './README/gen_readme.py' -f 'pdf,html,md' -l "M0"

git add README 
git add README.pdf
git add README.md

git commit -m "$commit_message"
git push origin master