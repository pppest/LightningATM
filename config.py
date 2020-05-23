from configparser import ConfigParser
import logging
import os
import math
from shutil import copyfile
import utils

#import atm_logger

display = 'touchscreen' ## options: eink_papirus, touchscreen

home = os.path.expanduser("~")
ATM_data_dir = home + "/.lightningATM/"
config_file_path = ATM_data_dir + "config.ini"

# check the config directory exists, create it if not
if not os.path.exists(ATM_data_dir):
    os.makedirs(ATM_data_dir)

# Configure basigConfig for the "logging" module
logging.basicConfig(
    filename="{}/debug.log".format(ATM_data_dir),
    format="%(asctime)-23s %(name)-9s %(levelname)-7s | %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    level=logging.DEBUG,
)

# Create logger for this config file
logger = logging.getLogger("CONFIG")

yes = ["yes", "ye", "y"]
no = ["no", "n"]


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
BTCPRICE = utils.get_btc_price('btc') ##conf["atm"]["cur"])
SATPRICE = math.floor((1 / (BTCPRICE * 100)) * 100000000)

# Button / Acceptor Pulses
LASTIMPULSE = 0
PULSES = 0
LASTPUSHES = 0
PUSHES = 0

# Lists for different coin counting, not yet implemented
# COINLIST = []
# PULSLIST = []
