import logging
import time

from lib.olsanka.olsanka import Olsanka


logging.getLogger().setLevel(logging.INFO)


class Flow:
    def __init__(self, browser):
        logging.info('__init__')
        self.browser = browser
        self.olsanka_instance = Olsanka(browser)
    
    def login_and_find_next_free_and_book(self):
        logging.info('login_and_find_next_free_and_book')

        #time.sleep(1)
        self.olsanka_instance.login()

        self.olsanka_instance.switch_view_to_badminton()
        #time.sleep(1)
        next_free = self.olsanka_instance.find_next_free()
        #time.sleep(1)
        self.olsanka_instance.book()
    