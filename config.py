from configparser import ConfigParser
import logging
import os
import math
from shutil import copyfile
import utils
import atm_logger

display = 'touchscreen' ## options: eink_papirus, touchscreen

home = os.path.expanduser("~")
ATM_data_dir = home + "/.lightningATM/"
config_file_path = ATM_data_dir + "config.ini"

# check the config directory exists, create it if not
if not os.path.exists(ATM_data_dir):
    os.makedirs(ATM_data_dir)

CONFIG_FILE = atm_logger.get_config_file()
conf = atm_logger.create_config()

######################################################
### (Do not change and of these parameters unless  ###
### you know exactly what you are doing.           ###
######################################################

# TODO: Add variable to set certificate check to true or false

# Papirus eInk size is 128 x 96 pixels
# WHITE = 1
# BLACK = 0
# PAPIRUSROT = 0
# PAPIRUS = Papirus(rotation=PAPIRUSROT)

# API URL for coingecko
COINGECKO_URL_BASE = "https://api.coingecko.com/api/v3/"

# Fiat and satoshi variables
FIAT = 0
SATS = 0
SATSFEE = 0
INVOICE = ""

# Set btc and sat price
BTCPRICE = utils.get_btc_price(conf["atm"]["cur"])
SATPRICE = math.floor((1 / (BTCPRICE * 100)) * 100000000)

# Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0

# Lists for different coin counting, not yet implemented
# COINLIST = []
# PULSLIST = []
