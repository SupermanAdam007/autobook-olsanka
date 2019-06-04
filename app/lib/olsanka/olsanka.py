import logging

import pandas as pd

from lib.browser import Browser
from lib.img import MyImage


logging.getLogger().setLevel(logging.INFO)


class UnknownStateFromColor(Exception):
    pass


class CellStates:
    BOOKED = 'BOOKED'
    FREE = 'FREE'
    BANNED = 'BANNED'


class ColorFieldStateMapping:
    BOOKED = ['#0033CC', '#3300CC']
    FREE = ['#FFFFFF']
    BANNED = ['#D1D1D1']

    @staticmethod
    def get_state_from_hex_color(hex_color):
        if hex_color in ColorFieldStateMapping.BANNED:
            return CellStates.BANNED
        elif hex_color in ColorFieldStateMapping.BOOKED:
            return CellStates.BOOKED
        elif hex_color in ColorFieldStateMapping.FREE:
            return CellStates.FREE
        else:
            raise UnknownStateFromColor(f'Color: {hex_color}')
            #logging.warn(f'do not know color: {hex_color}')


class AlreadyBookedStyle:

    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __str__(self):
        return str(self.__dict__)

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


class ScheduleDataField:

    def __init__(self, iid, is_free=True):
        self.iid = iid
        self.is_free = is_free


class Schedule:

    def __init__(self, iid: str, day: str, date: str, header_times: list, data):
        self.iid = iid
        self.day = day
        self.date = date
        self.header_times = header_times
        self.data = data

    @staticmethod
    def factory(schedule_webelement_table, already_booked_styles):
        return Schedule(
            iid='schedule_0',
            day='Út',
            date='4/6',
            header_times=[],
            data=[[],[]]

        )

    def __str__(self):
        return str(self.__dict__)


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
        for schedule_cell in self._get_all_cells():
            cell_img = MyImage(png_bytes=schedule_cell.screenshot_as_png)
            hex_color = cell_img.get_average_colour(return_hex=True)
            #cell_img.save_img(f'imgs/{hex_color.split("#")[1]}.png')

            cell_state = ColorFieldStateMapping.get_state_from_hex_color(hex_color)

            logging.info(schedule_cell.get_attribute('id') + ': ' + cell_state)


    def _get_all_cells(self):
        return self._browser.find_elements_by_class_name('scheduleCell')

    # @staticmethod
    # def _get_schedule_cells(schedule):
    #     return schedule.find_elements_by_class_name('scheduleCell')

    def _get_already_booked(self):
        res_container = self._browser.find_element_by_id('resContainer')
        res_events = res_container.find_elements_by_class_name('event')

        already_booked_styles = []
        for res_event in res_events:
            already_booked_styles.append(AlreadyBookedStyle.factory_from_event_style(
                res_event.get_attribute('style')))

        return already_booked_styles

    def _get_sport_schedules(self):
        return [x for x in self._browser.find_elements_by_class_name('schedule') if x.tag_name == 'table']

    def book(self, next_free):
        logging.info('book')
        logging.info(f'next_free: {next_free}')
