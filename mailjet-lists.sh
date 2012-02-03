#!/bin/bash
curl --user 807acc36b2f4763cc4e16e8a7b3fa945:c8f23ac9200c098f86a4cc5cae42ce19 \
	"http://api.mailjet.com/0.1/listsAll" | xmllint --format -
