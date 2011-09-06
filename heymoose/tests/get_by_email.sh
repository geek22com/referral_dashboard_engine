#!/bin/bash
email=$1
url=http://localhost:5500/users?email=$email
echo $url
curl -i $url
