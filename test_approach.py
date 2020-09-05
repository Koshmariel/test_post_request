from browsermobproxy  import Server
from selenium import webdriver
# import pprint  #for printing HAR
import json #for saving HAR



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

if "__main__" == __name__:
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    page_name = "ping.eu"
    #client.new_har("ping.eu")
    client.new_har(page_name, options = {'captureHeaders': True, 'captureContent': True})  #get request body

    PATH = "C:\Program Files (x86)\chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_argument("'--ignore-certificate-errors")

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    driver = webdriver.Chrome(PATH, chrome_options=options, desired_capabilities=capabilities)
    test_path = "https://ping.eu/ns-whois/"
    driver.get(test_path)


    # driver.get("https://csssr.github.io/qa-engineer/")


    print("TITLE=", driver.title)  # check if we are where we want us to be

    driver.implicitly_wait(5)

    text_field = driver.find_element_by_name("host")
    domain_name = "weird_domain_name.xyz"
    text_field.send_keys(domain_name)

    search_button = driver.find_element_by_name("go")
    search_button.click()

    driver.implicitly_wait(2)

    # save requests for convenient analysis
    with open('requests.json', 'w', encoding='utf-8') as f:
        json.dump(client.har, f, ensure_ascii=False, indent=4)

    #pprint.pprint(client.har) #with body requests it wil be quite big, better to save as json

    #har_values_lst = list(client.har.values())  # type(dict.values) is view, not list
    har_values_str = str(client.har.values())    # better to transform to string & search substring in it

    was_found = domain_name in har_values_str

    print(was_found)

    # should be changed to try-finally form
    # pytest/unitest class with setUp + tearDown methods will also be OK
    # if server is not stopped properly it will screw up with the system proxy settings
    server.stop()
    driver.quit()  # close browser