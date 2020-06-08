from selenium.webdriver import Firefox

class WebBrowser(Firefox):

    home_url = \
    "https://aplicaciones.iingen.unam.mx/AcelerogramasRSM/Consultas/FiltroAv.aspx"

    user_name = "yairgrmz.pe@gmail.com"

    def get_home(self):
        self.get(WebBrowser.home_url)

    def _send_keys_by_xpath(self, xpath, value):
        web_element = self.find_element_by_xpath(xpath)
        web_element.send_keys(value)

    def _click_element_by_xpath(self, xpath):
        web_element = self.find_element_by_xpath(xpath)
        web_element.click()

    def login_keys(self):
        self._send_keys_by_xpath('//*[@id="MainContent_tbCorrElec"]', WebBrowser.user_name)
        self._click_element_by_xpath('//*[@id="MainContent_btnIniciar"]')

    def query_ground_motions(self, initial_date, final_date):
        self._click_element_by_xpath('//*[@for="MainContent_chkSismo"]')
        self._send_keys_by_xpath('//*[@id="MainContent_dfFechaIni_txtDate"]', initial_date)
        self._send_keys_by_xpath('//*[@id="MainContent_dfFechaFin_txtDate"]', final_date)
        self._click_element_by_xpath('//*[@id="MainContent_btnBuscar"]')

    def download_files(self):
        self._click_element_by_xpath('//*[@id="MainContent_lbtnSeleccionTodo"]')
        self._click_element_by_xpath('//*[@for="MainContent_chkAgree"]')
        self._click_element_by_xpath('//*[@id="MainContent_btnDescargarASA"]')

if __name__ == "__main__":
    wb = WebBrowser()
    wb.get_home()
    wb.login_keys()
    wb.get_home()
    wb.query_ground_motions('01/01/2010', '01/01/2011')
    wb.download_files()
