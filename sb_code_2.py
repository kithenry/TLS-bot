#!/usr/bin/env python3

from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import json
import requests
import file_io  # your own module for reading accounts

TLS_URL = "https://visas-fr.tlscontact.com/"
CHECK_INTERVAL = 60
MAX_RETRIES = 4

accounts = file_io.read_json('customers.json')

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
CAPSOLVER_API_KEY = "CAP-YOUR_KEY_HERE"
driver = Driver(uc=True,user_data_dir='chrome_profile')

def random_delay():
    time.sleep(random.uniform(10, 16))


def check_visibility(driver):
    js = """
    return (document.body?.innerText?.toLowerCase().includes("you are human") ||
            document.body?.innerText?.toLowerCase().includes("verifying that you are human"));
"""
    is_still_on_cf = driver.execute_script(js)
    return is_still_on_cf

def solve_captcha(driver):
    retries = 0
    is_visible = check_visibility(driver)
    if not is_visible:
        print("No captcha here.. move on")
        return
    # Returns True if any visible element contains the phrase
    while is_visible and  retries<MAX_RETRIES:
        retries += 1
        driver.sleep(1)
        driver.uc_gui_click_captcha()
        is_visible = check_visibility(driver)
    [print("Captcha solved") if not is_visible else "Retry limit hit: Capture not solved" ]

    # try again 4 times if not visible then quit





# selection methods

def select_option_by_text(identifier, select_text):
    select_element = driver.find_element(By.ID,identifier)
    Select(select_element).select_by_visible_text(select_text)

#try block needed here
def click_element_by_text(driver,text):
    element = driver.find_element(By.XPATH,f"//*[normalize-space(text())='{text}']")
    driver.execute_script("""
    let el = arguments[0];
    el.scrollIntoView({block: 'center', inline: 'nearest'});
    let parent = el.offsetParent;
    while (parent) {
        parent.scrollTop = el.offsetTop - parent.offsetTop - parent.clientHeight/2;
        parent = parent.offsetParent;
    }
""", element)
    driver.execute_script("""
    let banner = document.querySelector('[aria-label="Cookie-Consent-Banner"]');
    if (banner) banner.style.display = 'none';
""")
    print("Tried to vanish cookie banner")
    driver.sleep(3)
    element.click()

# hard hack



def navigate_pre_login(driver):
    # wrap all click tasks in try except blocks
    # there are times when , we are not given a captcha
    # but the page is blank as if to say, it forgot a captcha and wants us
    # to refresh so it can give us one
    driver.click("#btn-apply-for-a-visa")
    print("Clicked 'Prendre un rendez-vous'")
    driver.sleep(1)

    driver.click("#btn-yes-uk-visa")
    print("Clicked 'Oui'")
    driver.sleep(1)

    driver.click("#btn-select-country")
    print("Clicked 'Sélectionner un pays'")

    select_option_by_text("select-country", "Égypte")
    print("Selected 'Égypte'")
    driver.sleep(1)

    driver.click("#btn-confirm-country")
    print("Clicked 'Confirmer'")
    driver.sleep(2)

def check_account(email, password):
    print(f"Checking account: {email}")
    driver.uc_open_with_reconnect(TLS_URL,2)
    driver.sleep(3)
    solve_captcha(driver)
    navigate_pre_login(driver)
    solve_captcha(driver)

    click_element_by_text(driver,"El-Sheikh Zayed")
    # hard hack to select center

    #elements = driver.find_elements("div.tls-simple-text")
    #if len(elements) >= 7:
    #    print(element[6])
    #    print("Clicked El-Sheikh Zayed")
    #else:
    #    print("Could not find enough elements to select center")
    #    return

    driver.sleep(4)
    solve_captcha(driver)
    driver.click("a.tls-button-link:contains('Login')", timeout=20)
    print("Clicked Login")

    driver.sleep(6)
    solve_captcha(driver)
    driver.type("#username", email)
    driver.type("#password", password)
    driver.click("#kc-login")
    print("Logged in!!")
    # check if we have been taken back to prelogin procedure stage
    # check group
    # check appointment
    # book appointment

    random_delay()

def main():
    if not accounts:
        print("No accounts found in customers.json")
        return
    check_account(accounts[0]["email"], accounts[0]["password"])

if __name__ == "__main__":
    main()
