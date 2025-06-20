# Youtube Insights Chrome Plugin documentation!

## Description

A chrome plugin to get Youtube insights using an end-to-end ML model built using MLFlow & DVC and deployed using Docker, CI/CD and AWS EC2, S3 & ECR.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://youtube-insights-chrome-plugin-dvc-bucket/data/`.
* `make sync_data_down` will use `aws s3 sync` to recursively sync files from `s3://youtube-insights-chrome-plugin-dvc-bucket/data/` to `data/`.


