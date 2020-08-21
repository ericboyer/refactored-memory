#!/bin/bash

function usage() {
  echo "usage: $(basename $0) <project> <cicd_project>"
  exit 1
}

# set dev and cicd tools project
[[ -z $1 ]] && PROJECT=refactored-memory || PROJECT=$1
[[ -z $2 ]] && CICD_PROJECT=ebo-cicd || PROJECT=$2

DEV_PROJECT="${PROJECT}-dev"
TEST_PROJECT="${PROJECT}-test"
PROD_PROJECT="${PROJECT}"

# create project namespace
for project in $DEV_PROJECT $TEST_PROJECT $PROD_PROJECT
do
  oc new-project "$project"
done

# create shared resources i.e., cm, rolebinding, etc.
oc process -f openshift/shared-template.yaml | oc -n "$DEV_PROJECT" create -f -

# create backend application
oc process -f openshift/backend-template.yaml \
  -p NAMESPACE="$DEV_PROJECT" \
  -p BRANCH="feature/7-rework-pipeline" | oc -n "$DEV_PROJECT" create -f -

# create frontend application
oc process -f openshift/frontend-template.yaml \
  -p NAMESPACE="$DEV_PROJECT" \
  -p BRANCH="feature/7-rework-pipeline" | oc -n "$DEV_PROJECT" create -f -

# create and start pipeline build
oc process -f openshift/pipeline.yaml -p BRANCH="feature/7-rework-pipeline" | oc -n $CICD_PROJECT create -f -

# kick off first pipeline build
oc -n $CICD_PROJECT start-build refactored-memory
