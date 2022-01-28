#! /bin/bash

sudo chmod 666 ./_posts/$1
python3 encoder.py _posts/$1 _posts/$1 $2