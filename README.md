# gqdc-chain-autorecover

This tool can be used to seamsly recover the Quadrans node software (gqdc) from error conditions due to local chain-data corruption.
The tool runs on Linux systems including its derived distributions for Single-Board-Computers (Raspbian OS, Armbian OS, etc.)

## Dependancies
The tools requires:
-	Python 3.6+ and Pip3
-	virtualenv

which can be installed by running:
```
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install virtualenv  
```
In addition, the gqdc client has to be already installed. It is suggested to do this operation  following the instructions provided by Quadrans' official documentation available [here](https://docs.quadrans.io/nodes/)

## Installation
Clone this repository through
```
git clone https://github.com/JacopoGrecuccio/gqdc-chain-autorecover.git
```
then run
```
cd gqdc-chain-autorecover/install
sudo bash install.sh
```
The default installation path is `/home/quadrans/gqdc-chain-autorecov` but you can modify it by properly changing the value of the variable `INSTALL_PATH` in both `install/install.sh` and `run.sh` prior running the install script.

### Gqdc required configurations

When the script runs gqdc-node needs to be correctly running and that its RPC port is correctly opened locally.
For further information about enabling RPC port on your node follow the instruction in the Appendix

## Environment file
The tool uses an environment (`gqdc-autorecov-env`) file which allow the user to set its system-specific parameters,
The file provides the following configurable variables:

-	`WEB3_RPC_PROVIDER` : a valid RPC url in the format `http://hostname-or-IP:port` at which your node is reachable through RPC (see RPC section above)
-	`CHAINDATA_STALE_TIME_SECS` : the number of seconds that must elaps since the last downloaded block for proceding with a chain-data reset
-	`GQDC_START_COMMAND` : the command used by the system to start the gqdc node
-	`GQDC_STOP_COMMAND` : the command used by the system to stop the gqdc node
-	`GQDC_CHAINDATA_PATH` : the file-system's path where gqdc's chaindata is stored

The default values for these parameters are the following:
```
export WEB3_RPC_PROVIDER="http://127.0.0.1:8545"
export CHAINDATA_STALE_TIME_SECS=18000 # Default is 5 hours
export GQDC_START_COMMAND="systemctl start quadrans-node"
export GQDC_STOP_COMMAND="systemctl stop quadrans-node"
export GQDC_CHAINDATA_PATH="/home/quadrans/.quadrans/gqdc/chaindata/*"
```
## Running the tool
If you didn't modified the installation path, you can run the tool by simply running
`sudo /home/quadrans/gqdc-chain-autorecov/run.sh`
otherwise you should locate `run.sh` in your custom installation path and run it.

For a better mantainance-automation of your Quadrans node, it is suggested to add this tool to your crontab for making it periodically check the chain-data in automatic.

**NOTE**: Remember that the script needs to be run as `sudo`

## Appendix : Enabling RPC communication port

For enabling a local RPC endpoint on your node you need to execute the binary with the `--rpc` option.
For example: `/usr/local/bin/gqdc --rpc ...other options..`

***If you used Quadrans' official installer*** to download and install your Quadrans node, you can follow the following steps for enabling the RPC endpoint.
```
sudo nano /home/quadrans/gqdc.sh
```
Change the line
```
eval "/usr/local/bin/gqdc ${GETH_PARAMS} ${MINER_OPTS} ${STATS_OPTS}"
```
in
```
eval "/usr/local/bin/gqdc --rpc --allow-insecure-unlock ${GETH_PARAMS} ${MINER_OPTS} ${STATS_OPTS}"
```
save and exit from the editor, then restart the node through:
```
sudo systemctl restart quadrans-node.service
```


**SECURITY DISCLAIMER**
If your node is configured for mining, and so it runs with `--unlock <wallet> --password <password_file>` enabled, it is strongly suggested to open the RPC endpoint only locally and to do not add cross-origin allowance by using `--rpccorsdomain` option unless you exactly know what your doing.
