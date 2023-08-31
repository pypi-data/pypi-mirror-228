#!/bin/bash

airflow db init
bash ./batch_files/scripts/build.sh
bash ./batch_files/scripts/venv.sh

python aws_batch_files\services\uploader.py all
python aws_batch_files\dags\creating_dag.py create
python aws_batch_files\dags\creating_dag.py import
#python aws_batch_files\dags\creating_dag.py instantiate
