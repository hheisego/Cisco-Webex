import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

def get_token(webex_user, password):
    # Selenium
    options = Options()
    options.add_argument('--headless')
    options.add_argument("start-maximized")
    certs = {"acceptInsecureCerts": True}
    options.set_capability("loggingPrefs", certs)
    service = Service('./geckodriver')

    browser = webdriver.Firefox(service=service, options=options)

    browser.get('https://<your server ip or domain>:5007/')
    time.sleep(1.7)
    input_grant = browser.find_element(by=By.ID, value='grant-button')
    input_grant.click()
    time.sleep(1.7)
    browser.find_element(by=By.ID, value="IDToken1").send_keys(webex_user)
    time.sleep(.7)
    browser.find_element(by=By.NAME, value="btnOK").click()
    time.sleep(1.7)
    browser.find_element(by=By.ID, value="IDToken2").send_keys(password)
    time.sleep(.7)
    browser.find_element(by=By.NAME, value="Login.Submit").click()
    time.sleep(1.7)
    access_token = browser.find_element(by=By.ID, value="access_token").get_attribute("value")
    refresh_token = browser.find_element(by=By.ID, value="refresh_token").get_attribute("value")

    print(access_token)
    print(refresh_token)
    browser.quit()

get_token(webex_user="webexaccount@mailservice.com", password="hheisego")