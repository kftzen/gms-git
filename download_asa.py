from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select

class WebBrowser(Firefox):

    home_url = \
    "https://aplicaciones.iingen.unam.mx/AcelerogramasRSM/Consultas/FiltroAv.aspx"

    user_name = "yairgrmz.pe@gmail.com"

    def __init__(self, download_dir):
        options = self._set_up_options(download_dir)
        super().__init__(options=options)

    def login(self):
        self._get_home()
        self._login_keys()

    def download(self, accel):
        accel = str(accel)
        self._get_home()
        self._query_ground_motions(accel)
        self._download_files()

    def _set_up_options(self, download_dir):
        options = Options()
        download_dir = str(download_dir)
        options.set_preference("browser.download.panel.shown", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_dir)
        return options

    def _get_home(self):
        self.get(WebBrowser.home_url)

    def _send_keys_by_xpath(self, xpath, value):
        web_element = self.find_element_by_xpath(xpath)
        web_element.send_keys(value)

    def _click_element_by_xpath(self, xpath):
        web_element = self.find_element_by_xpath(xpath)
        web_element.click()

    def _select_option_by_xpath(self, xpath, value):
        web_element = self.find_element_by_xpath(xpath)
        web_object = Select(web_element)
        web_object.select_by_value(value)

    def _login_keys(self):
        self._send_keys_by_xpath('//*[@id="MainContent_tbCorrElec"]', WebBrowser.user_name)
        self._click_element_by_xpath('//*[@id="MainContent_btnIniciar"]')

    def _query_ground_motions(self, acce):
        self._click_element_by_xpath('//*[@for="MainContent_chkAceleracion"]')
        self._select_option_by_xpath('//*[@id="MainContent_ddlAceleracionGal"]', '=')
        self._send_keys_by_xpath('//*[@id="MainContent_txtAcelGal"]', acce)
        self._click_element_by_xpath('//*[@id="MainContent_btnBuscar"]')

    def _download_files(self):
        self._click_element_by_xpath('//*[@id="MainContent_lbtnSeleccionTodo"]')
        self._click_element_by_xpath('//*[@for="MainContent_chkAgree"]')
        self._click_element_by_xpath('//*[@id="MainContent_btnDescargarASA"]')

if __name__ == "__main__":
    pass
