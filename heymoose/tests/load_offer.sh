#!/bin/bash
#url=http://heymoose.com/rest_api?methods=getOffers&uid=$1&app=$2&sig=$3
secret="26c10b40-47ae-416d-9788-b106c64a57d9"
sig=`echo "app_id=$1format=JSONmethod=getOffersuid=$2$secret" | md5sum | awk '{ print $1}'`
url="http://heymoose.com/rest_api/api?method=getOffers&app_id=$1&uid=$2&format=JSON&sig=2848b9630168f719b7c8724f06fc12dc"

echo $url
curl -i $url
