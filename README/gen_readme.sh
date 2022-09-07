#!/bin/bash
commit_message="$1"

python3 './README/gen_readme.py' --format 'pdf,html,md' --volume "M0"
