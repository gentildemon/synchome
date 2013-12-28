#!/bin/sh

BASEDIR=$(dirname $(readlink -f $0))

PYTHONPATH="$BASEDIR" python "$BASEDIR"/main.py