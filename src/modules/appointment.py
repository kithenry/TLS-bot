#!/usr/bin/env python3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Appointment:
    def __init__(self, driver, captcha_solver, clicker):
        self.driver = driver
        self.captcha_solver = captcha_solver
        self.clicker = clicker

    def solve_captcha(self):
        self.captcha_solver.solve()

    def go_to_group_page(self):
        try:
            # self.driver.click("//*[text()='My Application']")

            self.clicker.click_by_text("My Application")
            self.solve_captcha()

        except Exception as e:
            print(f"Error navigating to group page: {e}")

    def view_group(self):
        try:
            self.clicker.click_btn_content("VIEW GROUP")
            self.solve_captcha()

        except Exception as e:
            print(f"Error viewing group: {e}")

    def check_availability(self, timeout=10):
        try:
            # Wait for the popup to be present
            self.driver.execute_script("document.body.style.zoom='70%'")
            self.driver.sleep(3)
            self.clicker.click_btn_content("Book appointment")
            self.solve_captcha()
            self.driver.sleep(3)

            popup = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tls-popup"))
            )

            # Once present, locate the message div and check its text
            message_div = popup.find_element(
                By.XPATH, ".//div[contains(text(), 'no available appointment')]"
            )
            if message_div and "no available appointment" in message_div.text.lower():
                # Optionally click the Confirm button
                try:
                    confirm_button = popup.find_element(
                        By.XPATH, ".//button[@data-tls-value='confirm']"
                    )
                    confirm_button.click()
                except Exception:
                    pass  # If you want to silently skip if confirm not found
                print("No available appointments")
                return False  # Message found and optionally handled
            print("Inavailability popup not detected, appointments probably available")
            return True  # Popup not available, appointment probably present

        except TimeoutException:
            print("Check timeout error")
            return False  # Popup didn't appear in Sun Aug  3 01:21:51 2025

    def check_availability_bkup(self):
        try:
            self.driver.execute_script("document.body.style.zoom='70%'")
            self.driver.sleep(3)
            self.clicker.click_btn_content("Book appointment")
            self.solve_captcha()
            self.driver.sleep(3)
            if self.driver.execute_script(
                "return document.body?.innerText?.toLowerCase().includes('sorry, there is no available appointment')"
            ):
                print("Appointment not available")
                self.clicker.click_by_text("x")
                return False
            print("Appointment probably available")
            return True
        except Exception as e:
            print(f"Error checking appointment availability: {e}")
            return False
