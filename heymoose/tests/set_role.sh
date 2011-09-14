#!/bin/bash
data="role=$1"
echo $data
curl -X PUT -i --data "role=$1" http://localhost:5468/users/$2
#curl -i http://localhost:5468/user/$1
