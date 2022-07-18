#!/bin/bash

# [description]
#     look for external links in code, and check if any of them
#     are broken
#
# [usage]
#
#     ./.ci/check-links.sh $(pwd)
#

set -u -o pipefail

SOURCE_TO_CHECK=$1

# get all unique external links, with some exceptions
#
# * links to private resources
# * local resources
# * links that are templated and require evaluation of code
#
URLS=$(
    grep \
        -R \
        -o \
        --binary-files=without-match \
        --no-filename \
        -E '(http|https)://[^"` )>,\\<]+' \
        "${SOURCE_TO_CHECK}" \
    | grep -v '\$' \
    | grep -v '{' \
    | grep -v -E '\:[0-9]+$' \
    | grep -v 'auth.docker.io' \
    | grep -v "community.saturnenterprise.io/" \
    | grep -v 'demo.saturnenterprise.io' \
    | grep -v "https://github.com/saturncloud/docs/" \
    | grep -v "https://github.com/saturncloud/website/" \
    | grep -v "https://fonts." \
    | grep -v "https://www.kaggle.com/code/fahd09/eda-of-crime-in-chicago-2005-2016/notebook" \
    | grep -v "https://AA99999.us-east-2.aws.snowflakecomputing.com/console/login" \
    | grep -v -E "(http|https)://[0-9]+" \
    | grep -v 'localhost.' \
    | grep -v 'localtest.' \
    | sed 's/\.$//g' \
    | sort -u
)

echo "Checking URLs in ${SOURCE_TO_CHECK}"

ISSUES_FOUND=0
for url in ${URLS}; do
    printf "  * %s ..." "${url}"
    if curl \
        --output /dev/null \
        --silent \
        --head \
        --retry 3 \
        --fail \
        -H "From: dev@saturncloud.io" \
        -H "User-Agent: saturn-cloud-automation" \
        "${url}";
    then
        printf "OK\n"
        continue
    else
        printf "ERROR\n"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
done

echo ""
echo "Done checking URLs in ${SOURCE_TO_CHECK}. Found ${ISSUES_FOUND} issues."
echo ""

exit $ISSUES_FOUND
