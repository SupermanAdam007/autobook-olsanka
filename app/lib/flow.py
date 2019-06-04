import os
import logging
import time

from lib.olsanka.olsanka import Olsanka


logging.getLogger().setLevel(logging.INFO)


class InvalidLoginCredentials(Exception):
    pass


class Flow:
    def __init__(self, browser):
        logging.info('__init__')
        self.browser = browser
        self.olsanka_instance = Olsanka(browser)

    def _login(self):
        username = os.environ.get('OLSANKA_USERNAME')
        password = os.environ.get('OLSANKA_PASSWORD')

        if not username or not password:
            raise InvalidLoginCredentials(f'username" {username}, password: {password}')

        logging.info('_login')
        self.olsanka_instance.login(username, password)

    def _switch_view_to_badminton(self):
        logging.info('_switch_view_to_badminton')
        self.olsanka_instance.switch_view_to_badminton()

    def _find_next_free(self):
        logging.info('_find_next_free')
        return self.olsanka_instance.find_free_records()

    def _book(self, next_free):
        logging.info('_book')
        self.olsanka_instance.book(next_free)

    def login_and_find_next_free_and_book(self):
        logging.info('login_and_find_next_free_and_book')

        self._login()
        self._switch_view_to_badminton()

        time.sleep(3)

        next_free = self._find_next_free()
        self.olsanka_instance.book(next_free)
