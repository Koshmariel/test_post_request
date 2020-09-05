from browsermobproxy  import Server
from selenium import webdriver
import pytest
import time
# import pprint  #for printing HAR
# import json #for saving HAR



class ProxyManager:

    browsermobproxy_path = "D:/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

    def __init__(self):

        self.server = Server(ProxyManager.browsermobproxy_path)
        self.client = None #will be initialized manually for better control

    def start_server(self):
        self.server.start()
        return self.server

    def start_client(self):
        #disable certificate check
        self.client = self.server.create_proxy(params={"trustALLServers":"true"})
        return self.client

class TestPostCheck:
    def setup(self):
        self.proxy = ProxyManager()
        self.server = self.proxy.start_server()
        self.client = self.proxy.start_client()
        self.page_name = "csssr"
        self.client.new_har(self.page_name, options={'captureHeaders': True, 'captureContent': True})  #get request body

        self.PATH = "C:\Program Files (x86)\chromedriver.exe"

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--proxy-server={}".format(self.client.proxy))
        self.options.add_argument("'--ignore-certificate-errors")

        self.capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        self.capabilities['acceptSslCerts'] = True
        self.capabilities['acceptInsecureCerts'] = True

        self.driver = webdriver.Chrome(self.PATH, chrome_options=self.options, desired_capabilities=self.capabilities)
        self.test_path = "https://csssr.github.io/qa-engineer/"
        self.driver.get(self.test_path)


    def test_POST(self):
        print("TITLE=", self.driver.title)  # check if we are where we want us to be

        self.driver.implicitly_wait(5)

        self.weird_email = "weird_email@weird_server.xyz"
        self.email_field = self.driver.find_element_by_class_name("email")
        self.email_field.send_keys(self.weird_email)

        self.weird_text = "weird_text_weird_text"
        self.text_field = self.driver.find_element_by_class_name("description")
        self.text_field.send_keys(self.weird_text)

        self.submit_button = self.driver.find_element_by_tag_name("button")
        self.submit_button.click()

        time.sleep(2)  #it looks har is updated with a small delay

        self.har_values_str = str(self.client.har.values())    # better to transform to string & search substring in it

        assert (self.weird_email in self.har_values_str) and (self.weird_text in self.har_values_str)

    def teardown(self):

        self.server.stop()
        self.driver.quit()  # close browser