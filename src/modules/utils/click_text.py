#!/usr/bin/env python3
from selenium.webdriver.common.by import By


def click_text(driver, text):
    element = driver.find_element(By.XPATH, f"//*[normalize-space(text())='{text}']")
    driver.execute_script(
        """
    let el = arguments[0];
    el.scrollIntoView({block: 'center', inline: 'nearest'});
    let parent = el.offsetParent;
    while (parent) {
        parent.scrollTop = el.offsetTop - parent.offsetTop - parent.clientHeight/2;
        parent = parent.offsetParent;
    }
""",
        element,
    )
    driver.execute_script(
        """
    let banner = document.querySelector('[aria-label="Cookie-Consent-Banner"]');
    if (banner) banner.style.display = 'none';
"""
    )
    print("Tried to vanish cookie banner")
    driver.sleep(1)
    element.click()
