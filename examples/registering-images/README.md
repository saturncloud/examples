# Registering Images

This example illustrates how to write a script to register images in Saturn Cloud.

This example takes a CSV of images (passed in via an `IMAGES` environment variable).

The first column is the name of the image in ECR. The second is the name of the image in Saturn Cloud. We assume we want
to register images under the Saturn Cloud user that is running this script.

This script will query ECR for image tags for the image. For each tag, it will check if the image version exists in Saturn Cloud. If it does not - it will create the image version.

The script will NOT create images - those must already exist.
