import logging

import pandas as pd

from config import Config
from lib.browser import Browser
from lib.img import MyImage

logging.getLogger().setLevel(logging.INFO)


class UnknownStateFromColor(Exception):
    pass

class NoFreeRecord(Exception):
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
            #raise UnknownStateFromColor(f'Color: {hex_color}')
            logging.warn(f'do not know color: {hex_color}')


class ScheduleObj:

    def __init__(self, day_str, date_str, schedule_time_headers: list):
        self.day_str = day_str
        self.date_str = date_str
        self.schedule_time_headers = schedule_time_headers

    @staticmethod
    def factory_from_webelem(schedule_webelem):
        day_str = schedule_webelem.find_element_by_class_name(
            'schedule_table_day_header_cell').text.split(' ')[0]
        date_str = schedule_webelem.find_element_by_class_name('header_date_part').text
        schedule_time_headers = [x.text for x in schedule_webelem.find_elements_by_class_name('scheduleTimeHeader')]
        return ScheduleObj(day_str, date_str, schedule_time_headers)

    def __str__(self):
        return str(self.__dict__)


class Record:

    def __init__(self, kurt_id, hour_id, state: CellStates, schedule_obj: ScheduleObj):
        self.kurt_id = kurt_id
        self.hour_id = hour_id
        self.state = state
        self.schedule_obj = schedule_obj

    def get_time_str(self):
        return self.schedule_obj.schedule_time_headers[self.hour_id]

    @staticmethod
    def factory(cell_id: str, state, schedule_webelem):
        cell_id_splitted = cell_id.split('_')
        kurt_id = int(cell_id_splitted[3])
        hour_id = int(cell_id_splitted[4])

        return Record(
            kurt_id=kurt_id,
            hour_id=hour_id,
            state=state,
            schedule_obj=ScheduleObj.factory_from_webelem(schedule_webelem)
        )

    def __str__(self):
        return str(self.__dict__)


class Olsanka:

    def __init__(self, browser: Browser, url='http://olsanka.e-rezervace.cz'):
        logging.info('__init__')
        self._browser = browser.browser_instance
        self._browser.get(url)

    def login(self, username='test_username', password=''):
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

    def find_free_records(self):
        logging.info('find_next_free')
        free_records = []
        for schedule_cell in self._get_all_cells():
            cell_img = MyImage(png_bytes=schedule_cell.screenshot_as_png)
            hex_color = cell_img.get_average_colour(return_hex=True)
            #cell_img.save_img(f'imgs/{hex_color.split("#")[1]}.png')
            cell_state = ColorFieldStateMapping.get_state_from_hex_color(hex_color)

            if cell_state == CellStates.FREE:
                logging.info(schedule_cell.get_attribute('id') + ': ' + cell_state)
                cell_id = schedule_cell.get_attribute('id')
                free_records.append(Record.factory(
                    cell_id=cell_id,
                    state=cell_state,
                    schedule_webelem=self.get_schedule_webelem_from_cell_id(cell_id)
                ))

        return free_records

    def _get_all_cells(self):
        return self._browser.find_elements_by_class_name('scheduleCell')

    def filter_unwanted(self, free_records):
        possible_days = Config.POSSIBLE_DAYS
        possible_hours = Config.POSSIBLE_HOURS

        free_filtered = []
        for free_record in free_records:
            if free_record.get_time_str() in possible_hours \
                    and free_record.schedule_obj.day_str in possible_days:
                free_filtered.append(free_record)

        return free_filtered

    def get_schedule_webelem_from_cell_id(self, cell_id):
        cell_id_splitted = cell_id.split('_')
        return self._browser.find_element_by_id(f'schedule_{cell_id_splitted[1]}')

    def book(self, next_free):
        logging.info('book')

        next_free = self.filter_unwanted(next_free)
        if not next_free:
            raise NoFreeRecord()

        for x in next_free:
            logging.info(f'next_free: {x}')

