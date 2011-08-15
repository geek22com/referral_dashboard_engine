#!/bin/sh
PREFIX=HEYMOOSE
CURRENT_TIME=`date +%Y-%m-%d-%k:%M:%S`
CURRENT_HOST=`hostname`
DATABASE_NAME=social_sampler
SCHEMA_DUMP_NAME=$PREFIX"-schema_dump-"$CURRENT_HOST"-"$DATABASE_NAME"-"$CURRENT_TIME

echo "...Going to dump "$DATABASE_NAME" schema to "$SCHEMA_DUMP_NAME
pg_dump --schema-only -h localhost -U qa --password $DATABASE_NAME > $SCHEMA_DUMP_NAME
