#!/bin/bash
data="userId=$1&title=$2&body=$3&balance=$4&cpa=$5" 
echo $data
curl -X POST -i --data $data http://localhost:5468/orders
