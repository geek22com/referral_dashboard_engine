#!/bin/bash
iconv -f cp1251 -t utf8 $1 > $1.tmp
mv $1.tmp $1
