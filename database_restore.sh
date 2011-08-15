#!/bin/sh
RESTORE_FROM=$1
if [ ! -n "$RESTORE_FROM" ]
then
echo "Error: "$0" <restore_from_file>"
exit 0
fi

PREFIX=HEYMOOSE
CURRENT_TIME=`date +%Y-%m-%d-%k:%M:%S`
CURRENT_HOST=`hostname`
DATABASE_NAME=social_sampler
DATA_DUMP_NAME=$PREFIX"-data_dump-"$CURRENT_HOST"-"$DATABASE_NAME"-"$CURRENT_TIME

echo "...Going to dump "$DATABASE_NAME" to "$DATA_DUMP_NAME
pg_dump -h localhost -U qa --password $DATABASE_NAME > $DATA_DUMP_NAME

psql -h localhost -U qa --password $DATABASE_NAME < $RESTORE_FROM

