#!/bin/bash

os_type=$(uname -s)
echo $os_type

if [ "$os_type" = "Linux" ]; then
    source ./venv/bin/activate
    echo "> Activated source for $os_type"
else
    source ./venv/Scripts/activate
fi

