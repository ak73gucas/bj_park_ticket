#!/bin/bash
work_path=`pwd`"/"`dirname $0`
echo "work_path: $work_path"

cd $work_path

python src/yikatong.py
