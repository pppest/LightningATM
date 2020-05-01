
#import RPi.GPIO as GPIO
import logging
import os
import requests
import sys
import config
import math
# import qr


from PIL import ImageFont
from pathlib import Path

logger = logging.getLogger("UTILS")

led = "off"


## just copy pasted the methods here better check if all is good


def coins_inserted():
    """Actions coins inserted
    """
    global led

    if config.FIAT == 0:
        config.BTCPRICE = utils.get_btc_price(config.conf["atm"]["cur"])
        config.SATPRICE = math.floor((1 / (config.BTCPRICE * 100)) * 100000000)
        logger.info("Satoshi price updated")

    if config.PULSES == 2:
        config.FIAT += 0.02
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("2 cents added")
        display.update_amount_screen()
    if config.PULSES == 3:
        config.FIAT += 0.05
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("5 cents added")
        display.update_amount_screen()
    if config.PULSES == 4:
        config.FIAT += 0.1
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("10 cents added")
        display.update_amount_screen()
    if config.PULSES == 5:
        config.FIAT += 0.2
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("20 cents added")
        display.update_amount_screen()
    if config.PULSES == 6:
        config.FIAT += 0.5
        config.SATS = utils.get_sats()
        config.SATSFEE = utils.get_sats_with_fee()
        config.SATS -= config.SATSFEE
        logger.info("50 cents added")
        display.update_amount_screen()
    if config.PULSES == 7:
        config.FIAT += 1
        config.SATS = utils.get_sats()
        logger.info("100 cents added")
        display.update_amount_screen()
    config.PULSES = 0

    if config.FIAT > 0 and led == "off":
        # Turn on the LED after first coin
        GPIO.output(13, GPIO.HIGH)
        led = "on"
        logger.info("Button-LED turned on (if connected)")

def monitor_coins_and_button():
    """Monitors coins inserted and buttons pushed
    """
    global led
    time.sleep(0.2)
    if (time.time() - config.LASTIMPULSE > 0.5) and (config.PULSES > 0):
        coins_inserted(led)

    # Detect if the button has been pushed
    if (time.time() - config.LASTPUSHES > 1) and (config.PUSHES > 0):
        button_pushed()

def button_pushed():
    """Actions button pushes by number
    """
    if config.PUSHES == 1:
        """If no coins inserted, update the screen.
        If coins inserted, scan a qr code for the exchange amount
        """
        if config.FIAT == 0:
            display.update_nocoin_screen()
            time.sleep(3)
            display.update_startup_screen()

        if not config.conf["atm"]["activewallet"]:
            logger.error("No wallet has been configured for the ATM.")
            # Softreset and startup screen
            softreset()

        if config.conf["atm"]["activewallet"] == "btcpay_lnd":
            display.update_qr_request()
            qrcode = qr.scan()
            config.INVOICE = lndrest.evaluate_scan(qrcode)
            while config.INVOICE is False:
                display.update_qr_failed()
                time.sleep(1)
                display.update_qr_request()
                qrcode = qr.scan()
                config.INVOICE = lndrest.evaluate_scan(qrcode)
            display.update_payout_screen()
            lndrest.handle_invoice()
            softreset()
        elif config.conf["atm"]["activewallet"] == "lntxbot":
            lntxbot.process_using_lnurl(config.SATS)
            # Softreset and startup screen
            softreset()
            # lntxbot.payout(config.SATS, config.INVOICE)
        else:
            pass

    if config.PUSHES == 3:
        """Scan and store new wallet credentials
        """
        # Delete current wallet flag and credentials
        config.update_config("atm", "activewallet", "")
        config.update_config("lntxbot", "creds", "")
        config.update_config("lnd", "macaroon", "")

        display.update_wallet_scan()
        qr.scan_credentials()
        importlib.reload(config)

        if config.conf["atm"]["activewallet"] == "btcpay_lnd":
            display.update_btcpay_lnd()
        elif config.conf["atm"]["activewallet"] == "lntxbot":
            balance = lntxbot.get_lnurl_balance()
            display.update_lntxbot_balance(balance)
        else:
            logger.error("Scanning of wallet credentials failed.")

        softreset()

    if config.PUSHES == 4:
        """Simulates adding a coin
        """
        logger.info("Button pushed four times (add coin)")
        print("Button pushed four times (add coin)")
        config.PULSES = 2

    if config.PUSHES == 6:
        """Shutdown the host machine
        """
        display.update_shutdown_screen()
        GPIO.cleanup()
        logger.warning("ATM shutdown (6 times button)")
        os.system("sudo shutdown -h now")
    config.PUSHES = 0



def softreset():
    """Displays startup screen and deletes fiat amount
    """
    global led
    config.SATS = 0
    config.FIAT = 0
    # Turn off button LED
    GPIO.output(13, GPIO.LOW)
    led = "off"

    display.update_startup_screen()
    logger.info("Softreset executed")


def button_event(channel):
    """Registers a button push event
    """
    config.LASTPUSHES = time.time()
    config.PUSHES = config.PUSHES + 1


def coin_event(channel):
    """Registers a coin insertion event
    """
    config.LASTIMPULSE = time.time()
    config.PULSES = config.PULSES + 1


def setup_coin_acceptor():
    """Initialises the coin acceptor parameters and sets up a callback for button pushes
    and coin inserts.
    """
    # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO Pins for coin acceptor, button and button-led
    GPIO.setwarnings(False)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=300)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=coin_event)


def check_epd_size():
    """Check EPD_SIZE is defined
    """
    if os.path.exists("/etc/default/epd-fuse"):
        exec(open("/etc/default/epd-fuse").read(), globals())

    if EPD_SIZE == 0.0:
        print("Please select your screen size by running 'papirus-config'.")
        sys.exit()


def create_font(font, size):
    """Create fonts from resources
    """
    # Construct paths to foder with fonts
    pathfreemono = Path.cwd().joinpath("resources", "fonts", "FreeMono.ttf")
    pathfreemonobold = Path.cwd().joinpath("resources", "fonts", "FreeMonoBold.ttf")
    pathsawasdee = Path.cwd().joinpath("resources", "fonts", "Sawasdee-Bold.ttf")

    if font == "freemono":
        return ImageFont.truetype(pathfreemono.as_posix(), size)
    if font == "freemonobold":
        return ImageFont.truetype(pathfreemonobold.as_posix(), size)
    if font == "sawasdee":
        return ImageFont.truetype(pathsawasdee.as_posix(), size)
    else:
        print("Font not available")


def get_btc_price(fiat_code):
    """Get BTC -> FIAT conversion
    """
    url = config.COINGECKO_URL_BASE + "simple/price"
    price = requests.get(
        url, params={"ids": "bitcoin", "vs_currencies": fiat_code}
    ).json()
    return price["bitcoin"][fiat_code]


def get_sats():
    return config.FIAT * 100 * config.SATPRICE


def get_sats_with_fee():
    return math.floor(config.SATS * (float(config.conf["atm"]["fee"]) / 100))
