#!/bin/bash
id=$1
url=http://localhost:5468/apps/$id
echo $url
curl -i $url
