#!/usr/bin/env python3

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Login:
    def __init__(self, driver, captcha_solver, safe_clicker):
        self.driver = driver
        self.captcha_solver = captcha_solver
        self.clicker = safe_clicker

    def login(self, email, password):
        if self.driver.execute_script(
            "return document.body?.innerText?.toLowerCase().includes('my application')"
        ):
            print("Already logged in")
            return [True, False]
        try:
            # to wrap later
            self.driver.click("a.tls-button-link:contains('Login')", timeout=20)
            print("Clicked Login")
            self.driver.sleep(3)
            self.captcha_solver.solve()
            self.driver.type("#username", email)
            self.driver.type("#password", password)
            # self.driver.click("#kc-login")
            self.clicker.click_by_id("kc-login")
            print("Logging in")
            self.captcha_solver.solve()
            return [False, False]
        except Exception as e:
            print(f"Login failed: {e}")
            return [False, True]
