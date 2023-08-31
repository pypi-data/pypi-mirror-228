#!/bin/bash
# export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
gcloud config set project dozi-data-science-research-1
bash ./batch_files/scripts/build.sh
gaia-cli upload-batch-files all
# python ./batch_files/workflow/auto_scaling_policy.py
gaia-cli workflow-template create
gaia-cli dag create
# gaia-cli dag import
# gaia-cli workflow-template instantiate
gcloud config set project dozi-stg-ds-apps-1
