#!/bin/bash

label=refactored-memory

# set defaults for dev and cicd tools project
[[ -z $DEV_PROJECT ]] && DEV_PROJECT=refactored-memory-dev
[[ -z $CICD_PROJECT ]] && CICD_PROJECT=ebo-cicd

oc delete bc -l build=${label} -n $CICD_PROJECT
oc delete all -l app=refactored-memory-frontend -n $DEV_PROJECT
oc delete all -l app=refactored-memory-backend -n $DEV_PROJECT
oc delete rolebinding edit -n $DEV_PROJECT
oc delete cm $label -n $DEV_PROJECT