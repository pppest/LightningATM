#!/usr/bin/python3

import logging
import config
import utils
import os
import sys


#logger = logging.getLogger("MAIN")
#utils.setup_coin_acceptor()

## start Kivy version
if config.display == 'touchscreen':
    from displays import touchscreen
    touchscreen.run()

# ## start papyrus version
# elif config.display == 'papirus':
#     from displays import eink_papirus
#     eink_papirus.run()
#
# else:
#     Print('no screen chosen')
