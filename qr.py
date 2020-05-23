#!/usr/bin/python3

import zbarlight
import pyzbar
import logging
import requests
import time
import config
import cv2

from PIL import Image
from io import BytesIO
# from picamera import PiCamera

logger = logging.getLogger("QR")

def scan():
    if config.CAMERA =='USB':
        scan_usb_cam()
    elif config.CAMERA == 'PiCamera':
        scan_picam()


def scan_usb_cam():
    barcode_data = ""
    print("Scan wallet QR code")
    capture = cv2.VideoCapture(0)
    start = time.time()

    while(capture.isOpened()):
        ret, frame = capture.read()
        if ret is True:
            # check for qrcode and write if found and exit
            barcodes = zbarlight.scan_codes("qrcode",frame)
            # loop over the detected barcodes
        #     for barcode in barcodes:
        #         # extract the bounding box location of the barcode and draw the
        #         # bounding box surrounding the barcode on the image
        #         (x, y, w, h) = barcode.rect
        #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #         # the barcode data is a bytes object so if we want to draw
        #         # it on
        #         # our output image we need to convert it to a string first
        #         barcode_data = barcode.data.decode("utf-8")
        #         barcode_type = barcode.type
        #         # print the barcode type and data to the terminal
        #         print("Found {} barcode: {}".format(barcode_type, barcode_data))
        #         ## Make sure its a devault wallet
        #
        #     if barcodes != []:
        #             break
        # else:
        #     break
    capture.release()
    cv2.destroyAllWindows()
    return barcode_data

def scan_picam():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            logger.info("Start scanning for QR code")
        except:
            logger.error("PiCamera.start_preview() raised an exception")

        stream = BytesIO()
        qr_codes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10
        while qr_codes is None and (time.time() < timeout):
            stream.seek(0)
            # Start camera stream (make sure RaspberryPi camera is focused correctly
            # manually adjust it, if not)
            camera.capture(stream, "jpeg")
            qr_codes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()
        # break immediately if we didn't get a qr code scan
        if not qr_codes:
            logger.info("No QR within 10 seconds detected")
            return False

        # decode the first qr_code to get the data
        qr_code = qr_codes[0].decode()

        return qr_code


def scan_attempts(target_attempts):
    """Scan and evaluate users credentials
    """
    attempts = 0
    if config.CAMERA == 'PiCamera':

        while attempts < target_attempts:
            qrcode = scan_picam()
            if qrcode:
                logger.info("QR code successfuly detected.")
                return qrcode
            else:
                attempts += 1
                logger.error("{}. attempt!".format(attempts))

        logger.error("{} failed scanning attempts.".format(target_attempts))

    elif config.CAMERA == 'USB':

        while attempts < target_attempts:
            qrcode = scan_usb_cam()
            if qrcode:
                logger.info("QR code successfuly detected.")
                return qrcode
            else:
                attempts += 1
                logger.error("{}. attempt!".format(attempts))

        logger.error("{} failed scanning attempts.".format(target_attempts))



def scan_credentials():
    credentials = scan_attempts(4)

    if credentials:
        if ("lnd-config" in credentials) and ("lnd.config" in credentials):
            logger.info("BTCPayServer LND Credentials detected.")
            try:
                r = requests.get(credentials.lstrip("config="))
                data = r.json()
                data = data["configurations"][0]

                config.update_config("btcpay", "url", data["uri"] + "v1")
                config.update_config("lnd", "macaroon", data["adminMacaroon"])
                config.update_config("atm", "activewallet", "btcpay_lnd")
            except:
                logger.error("QR not valid (they expire after 10 minutes)")

        elif ("lntxbot" in credentials) and ("@" in credentials):
            logger.info("Lntxbot Credentials detected.")

            config.update_config("lntxbot", "creds", credentials.split("@")[0])
            config.update_config("lntxbot", "url", credentials.split("@")[1])
            config.update_config("atm", "activewallet", "lntxbot")

        else:
            logger.error("No credentials to a known wallet detected.")
    else:
        logger.error("No credentials to a known wallet could be detected.")
