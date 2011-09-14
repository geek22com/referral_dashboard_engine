#!/bin/bash
id=$1
#url=http://localhost:5500/users/$id?full=false
url=http://localhost:5468/users/$id?full=false
echo $url
curl -i $url
