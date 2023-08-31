#!/bin/bash

# This file is intended to initialize the cluster to a desired state. For example:
# python -m nltk.downloader -d venv/nltk_data all

# install python 3.9
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  -O miniconda.sh \
    && /bin/bash miniconda.sh -b -p $HOME/conda

echo -e '\n export PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

rm miniconda.sh

conda config --set always_yes yes --set changeps1 no
conda config -f --add channels conda-forge

conda create -n myenv python=3.9 -y
conda init bash
conda update -n base -c defaults conda
source activate myenv

sudo ln -s $(which python) /usr/bin/python3.9

ls -l /usr/bin/python3.9

pyspark --version

# Install Python requirements from S3 bucket
aws s3 cp s3://gaia-aws-airflow-try/testAROA2RVWNELOGORL4LZUO_ori/main/requirements_docker.txt requirements_docker.txt
pip install -r requirements_docker.txt
pip install --upgrade pyspark

pyspark --version

python -m pip show pyspark

