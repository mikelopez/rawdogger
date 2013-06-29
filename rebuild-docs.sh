#!/bin/bash
echo $1
if [ -z "$1" ]; then
    echo "Syntax: ./rebuild-docs /tmp/absolute-path-output/"
    exit 
fi

epydoc -v -v -v --html --output=$1 --inheritance=listed --css=white --graph=all xxxgalleries
