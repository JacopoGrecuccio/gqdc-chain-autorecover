#!/usr/bin/bash
INSTALL_PATH=/home/quadrans/gqdc-chain-autorecov

source ${INSTALL_PATH}/venv/bin/activate
source ${INSTALL_PATH}/gqdc-autorecov-env
python3 ${INSTALL_PATH}/src/main.py
deactivate
