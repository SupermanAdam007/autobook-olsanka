import logging

from pyvirtualdisplay import Display
from selenium import webdriver


logging.getLogger().setLevel(logging.INFO)


class Browser:
    def __init__(self, display_size=(800, 600), display_visible=False):
        self._display = Display(visible=1 if display_visible else 0, size=display_size)
        self._display.start()
        logging.info('Initialized virtual display..')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        #chrome_options.add_experimental_option('prefs', {
        #    'download.default_directory': os.getcwd(),
        #    'download.prompt_for_download': False,
        #})
        logging.info('Prepared chrome options..')

        self.browser_instance = webdriver.Chrome(chrome_options=chrome_options)
        logging.info('Initialized chrome browser..')
    
    def close(self):
        logging.info('Closing the browser..')
        self.browser_instance.quit()
        self._display.stop()
