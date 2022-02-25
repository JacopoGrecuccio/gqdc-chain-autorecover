PYTHON_CMD=python3
PIP_CMD=pip3

INSTALL_PATH=/home/quadrans/gqdc-chain-autorecov

# Cleanup
echo "Removing old installations..."
rm -Rf ${INSTALL_PATH}


# Create directory tree
echo "Building directory tree..."
mkdir -p ${INSTALL_PATH}
mkdir -p ${INSTALL_PATH}/src


echo "Installing dependancies..."
# Create and activate a virtualenv
virtualenv ${INSTALL_PATH}/venv
source ${INSTALL_PATH}/venv/bin/activate
# Install virtualenv requirements
${PIP_CMD} install -r ./requirements.txt
deactivate

echo "Copying files.."
# Copy env,sources,run-script
cp ../run.sh ${INSTALL_PATH}
cp ../gqdc-autorecov-env ${INSTALL_PATH}
cp ../src/main.py ${INSTALL_PATH}/src

echo "Installation completed. Run $INSTALL_PATH/run.sh to start the chain
auto-recover script or add it to your crontab for better automation"
