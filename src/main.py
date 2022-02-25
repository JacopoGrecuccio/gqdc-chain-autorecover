#!/usr/bin/python3
import logging
import os
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
# ------------------------------------------------------------------------------
# Configurable parameters, use the environment file to set their value
# ------------------------------------------------------------------------------


try:
    if os.environ["WEB3_IPC_PROVIDER"]!="":
        WEB3_IPC_PROVIDER=os.environ["WEB3_IPC_PROVIDER"]
    else:
        WEB3_IPC_PROVIDER="/home/quadrans/.quadrans/gqdc.ipc"
except KeyError:
    WEB3_IPC_PROVIDER="/home/quadrans/.quadrans/gqdc.ipc"
    pass

try:
    if os.environ["CHAINDATA_STALE_TIME_SECS"]!="":
        CHAINDATA_STALE_TIME_SECS=int(os.environ["CHAINDATA_STALE_TIME_SECS"])
    else:
        CHAINDATA_STALE_TIME_SECS=(5*60*60) # Default is 5 hours
except KeyError:
    CHAINDATA_STALE_TIME_SECS=(5*60*60) # Default is 5 hours
    pass

try:
    if os.environ["GQDC_START_COMMAND"]!="":
        GQDC_START_COMMAND=os.environ["GQDC_START_COMMAND"]
    else:
        GQDC_START_COMMAND="systemctl start quadrans-node"
except KeyError:
    GQDC_START_COMMAND="systemctl start quadrans-node"
    pass

try:
    if os.environ["GQDC_STOP_COMMAND"]!="":
        GQDC_STOP_COMMAND=os.environ["GQDC_STOP_COMMAND"]
    else:
        GQDC_STOP_COMMAND="systemctl stop quadrans-node"
except KeyError:
    GQDC_STOP_COMMAND="systemctl stop quadrans-node"
    pass

try:
    if os.environ["GQDC_CHAINDATA_PATH"]!="":
        GQDC_CHAINDATA_PATH=os.environ["GQDC_CHAINDATA_PATH"]
    else:
        GQDC_CHAINDATA_PATH="/home/quadrans/.quadrans/chaindata/*"
except KeyError:
    GQDC_CHAINDATA_PATH="/home/quadrans/.quadrans/chaindata/*"
    pass

# ------------------------------------------------------------------------------

logging.basicConfig()
logger = logging.getLogger("GQDCChainAutoRecov")

def main():
    logger.info("Started")
    # Connect to gqdc using IPC port
    w3 = Web3(Web3.HTTPProvider("http:127.0.0.1:8545"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if w3.isConnected():
        # Node is connected and correctly running
        if w3.eth.syncing!=False:
            # Node is not syncing
            lastBlock = w3.eth.get_block('latest')
            if (lastBlock["timestamp"]+CHAINDATA_STALE_TIME_SECS)<int(time.time()):
                # Chain is stale, we need to remove the chaindata and force
                # a resynch a the next node start-up
                os.system(GQDC_STOP_COMMAND)
                os.system("rm {}".format(GQDC_CHAINDATA_PATH))
                os.system(GQDC_START_COMMAND)
            else:
                # Chain valid
                logger.debug("Chaindata is valid")
        else:
            logger.warning("GQDC is syncing, giving up.")
    else:
        logger.error("Could not connect to node IPC port. Check your configuration file and ensure that GQDC is actually running")
    logger.info("Terminated")

if __name__=="__main__":
    main()
