#!/bin/bash
id=$1
curl -i -X DELETE http://localhost:5468/apps/$id
#curl -i http://localhost:5468/user/$1
