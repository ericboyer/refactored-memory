#!/bin/bash

function usage() {
  echo "usage: $(basename $0) [-p <project>][-c <cicd_project>][-b <branch>]"
  exit 1
}

# parse arguments
while getopts p:c:b flag
do
  case "${flag}" in
    p) PROJECT=${OPTARG};;
    c) CICD_PROJECT=${OPTARG};;
    b) BRANCH=${OPTARG};;
  esac
done

# set defaults for dev and cicd tools project
[[ -z $PROJECT ]] && PROJECT=refactored-memory
[[ -z $CICD_PROJECT ]] && CICD_PROJECT=ebo-cicd
[[ -z $BRANCH ]] && BRANCH=master

echo "PROJECT=$PROJECT"
echo "CICD_PROJECT=$CICD_PROJECT"
echo "BRANCH=$BRANCH"

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
  -p BRANCH="$BRANCH" | oc -n "$DEV_PROJECT" create -f -

# create frontend application
oc process -f openshift/frontend-template.yaml \
  -p NAMESPACE="$DEV_PROJECT" \
  -p BRANCH="$BRANCH" | oc -n "$DEV_PROJECT" create -f -

# create and start pipeline build
oc process -f openshift/pipeline.yaml -p BRANCH="$BRANCH" | oc -n $CICD_PROJECT create -f -

# kick off first pipeline build
oc -n $CICD_PROJECT start-build refactored-memory
