#!/bin/bash
curl -X POST -i --data "userId=$1" http://localhost:5468/apps
