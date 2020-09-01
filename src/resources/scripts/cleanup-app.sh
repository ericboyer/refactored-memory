#!/bin/bash

label=refactored-memory

# set defaults for dev and cicd tools project
[[ -z $DEV_PROJECT ]] && PROJECT=refactored-memory-dev
[[ -z $CICD_PROJECT ]] && CICD_PROJECT=ebo-cicd

for project in $CICD_PROJECT $DEV_PROJECT
do
  oc delete all -l build=${label}
done