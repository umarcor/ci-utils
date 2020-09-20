#!/bin/bash

: "${SIF_FILE:=image.sif}"
: "${DEF_FILE:=image.def}"

EXPECTED_FILE_TYPE="a /usr/bin/env run-singularity script executable (binary data)"
RECEIVED_FILE_TYPE=$(file $SIF_FILE | cut -d ":" -f 2 | sed -e 's/^[[:space:]]*//')

if [ "$EXPECTED_FILE_TYPE" != "$RECEIVED_FILE_TYPE" ]; then
	echo "Fatal error, $SIF_FILE header is a $RECEIVED_FILE_TYPE"
	echo "Showing first 100 chars of file received."
	head -c 100 $SIF_FILE
	exit 1
fi

DEF_SHA=$(md5sum $DEF_FILE | cut -d " " -f 1)
SIF_SHA=$(singularity sif dump 1 $SIF_FILE | md5sum | cut -d " " -f 1)

echo "$SIF_FILE: $SIF_SHA"
echo "$DEF_FILE: $DEF_SHA"

if [ "$DEF_SHA" == "$SIF_SHA" ]; then
	echo "$SIF_FILE is up-to-date with $DEF_FILE."
else
	echo "$SIF_FILE is out of date! Please rebuild it."
	exit 1
fi
