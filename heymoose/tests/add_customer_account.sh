#!/bin/bash
data="amount=$2" 
echo $data
curl -X PUT -i --data $data http://localhost:5468/users/$1/customer-account
