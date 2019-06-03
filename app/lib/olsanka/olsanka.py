import logging

import pandas as pd

from lib.browser import Browser

logging.getLogger().setLevel(logging.INFO)


class AlreadyBookedStyle:

    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __str__(self):
        return "left: " + self.left + ", top: " + self.top + ", width: " + self.width + ", height: " + self.height

    @staticmethod
    def factory_from_event_style(event_style):
        style_attrs = [x.strip() for x in event_style.split(';')]
        left = top = width = height = None

        for style_attr in style_attrs:
            attr = style_attr.split(': ')

            if len(attr) == 2:
                if attr[0] == 'left':
                    left = attr[1].split('px')[0]
                if attr[0] == 'top':
                    top = attr[1].split('px')[0]
                if attr[0] == 'width':
                    width = attr[1].split('px')[0]
                if attr[0] == 'height':
                    height = attr[1].split('px')[0]

        already_booked_style = None
        if left and top and width and height:
            already_booked_style = AlreadyBookedStyle(left, top, width, height)

        return already_booked_style


class Olsanka:

    def __init__(self, browser: Browser, url='http://olsanka.e-rezervace.cz'):
        logging.info('__init__')
        self._browser = browser.browser_instance
        self._browser.get(url)

    def login(self, username='karelkarel', password='afs)*$)!$)(XXx25)'):
        logging.info('login')
        self._input_login_credentials(username, password)
        self._browser.find_element_by_xpath(
            '//*[@id="webLoginForm"]/table/tbody/tr[4]/td/input[4]').click()

    def _input_login_credentials(self, username, password):
        logging.info(f'_input_login_credentials, username: {username}')
        input_username = self._browser.find_element_by_xpath('//*[@id="username"]')
        input_username.send_keys(username)
        input_username = self._browser.find_element_by_xpath('//*[@id="password"]')
        input_username.send_keys(password)

    def switch_view_to_badminton(self):
        badminton_button = self._browser.find_element_by_xpath(
            '//*[@id="cdForm:j_id251:1:serviceSelectButton"]')
        badminton_button.click()

    def find_next_free(self):
        logging.info('find_next_free')
        already_booked_styles = self._get_already_booked()
        logging.info(already_booked_styles)
        schedules = self._get_sport_schedules()
        for schedule in schedules:
            location = schedule.location
            size = schedule.size
            logging.info(schedule)

    def _get_already_booked(self):
        res_container = self._browser.find_element_by_id('resContainer')
        res_events = res_container.find_elements_by_class_name('event')

        already_booked_styles = []
        for res_event in res_events:
            already_booked_styles.append(AlreadyBookedStyle.factory_from_event_style(
                res_event.get_attribute('style')))

        return already_booked_styles

    def _get_sport_schedules(self):
        schedules = self._browser.find_elements_by_class_name('schedule')
        return schedules
        # dfs_schedules = []
        # for schedule in schedules:
        #     if schedule.tag_name == 'table':
        #         dfs_schedules.append(
        #             self._html_table_to_dataframe(schedule.get_attribute('outerHTML')))
        # return dfs_schedules

    # def _html_table_to_dataframe(self, html_table):
    #     return pd.read_html(html_table)

    def book(self):
        logging.info('book')
