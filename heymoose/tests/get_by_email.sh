#!/bin/bash
email=$1
url=http://localhost:5468/users?email=$email&full=true
echo $url
curl -i $url
