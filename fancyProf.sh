#!/bin/bash
python3 -m cProfile -o /tmp/profdata.pyprof puzzle.py $1
python3 -m pyprof2calltree -i /tmp/profdata.pyprof -o /tmp/profdata.callgrind
rm /tmp/profdata.pyprof
gprof2dot --format=callgrind --output=/tmp/out.dot /tmp/profdata.callgrind
rm /tmp/profdata.callgrind

TEMPFILE=$(mktemp --tmpdir XXXXX.svg)
NAME=$(basename "$TEMPFILE")

dot -Tsvg /tmp/out.dot -o ProfGraphs/$NAME 
rm /tmp/out.dot
chmod 775 ProfGraphs/$NAME
