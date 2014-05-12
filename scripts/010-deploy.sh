#!/bin/bash

set -u
set -e

# directory and branch of git repository with source data for jekyll.  
# Note: relative to parent directory, not to this directory (scripts/).
SOURCE_REPO='source'
SOURCE_BRANCH='gh-pages'

# directory and branch of git repository to commit output to.
# Note: relative to parent directory, not to this directory (scripts/).
TARGET_REPO='target'
TARGET_BRANCH='gh-pages'

TMP_DIR='_tmp_site_copy'

# pull source
cd $SOURCE_REPO
git checkout $SOURCE_BRANCH
git pull

# build site (ends up in _site)
jekyll build

# copy site to temporary directory
cd -
rm -rf $TMP_DIR
cp -R $SOURCE_REPO/_site $TMP_DIR

# switch to target repo and clear
cd $TARGET_REPO
git checkout $TARGET_BRANCH
rm -rf *

# copy in and remove temporary data
cd -
cp -r $TMP_DIR/* $TARGET_REPO
rm -rf $TMP_DIR

# commit and push
cd $TARGET_REPO
git add .
git commit -am 'generated'
git push