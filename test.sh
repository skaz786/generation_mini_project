#!/bin/bash
set -eu
project_dir="$HOME/OneDrive/Documents/pythongeneration/pythonminiproject/tests"
if [[ $(pwd) != ${project_dir} ]];
then
echo -e "Not in project directory.Changing directory to ${project_dir}\n"
cd ${project_dir}
fi
if pytest;
then
git commit -am "${1}"
fi