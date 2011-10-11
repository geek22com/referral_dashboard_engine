#!/bin/bash
app_id=$1
from_id=$2
to_id=$3
data="inviterExtId=$from_id&appId=$app_id&extId=$to_id"
curl -i -X POST --data $data http://localhost:5468/performers
