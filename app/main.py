import os
import logging
import time
import sys

from lib.browser import Browser
from lib.flow import Flow


logging.basicConfig(
      level=logging.INFO, 
      format='[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s',
      handlers=[logging.StreamHandler(sys.stdout)]
    )
log = logging.getLogger('Olsanka App')
log.setLevel(logging.INFO)


if __name__ == '__main__':
    browser = Browser(display_visible=True, display_size=(1000, 900))
    flow = Flow(browser)
    flow.login_and_find_next_free_and_book()
    time.sleep(5)
    browser.close()
