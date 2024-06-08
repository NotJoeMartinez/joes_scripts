#!/bin/bash
clipboard=$(pbpaste)

fname=$(echo $clipboard | tr -d '\n,@#' | inline-detox -s lower)
echo $fname | pbcopy
echo $fname

# Test String
# "FoO B&()\$#!ARR"