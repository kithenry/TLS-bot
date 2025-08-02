#!/usr/bin/env python3


class CaptchaSolver:
    def __init__(self, driver, max_retries=4):
        self.driver = driver
        self.max_retries = max_retries

    def check_visibility(self, text2check):
        js = f"""
        return (document.body?.innerText?.toLowerCase().includes("{text2check}") ||
                document.body?.innerText?.toLowerCase().includes("{text2check}"));
        """
        return self.driver.execute_script(js)

    def solve(self):
        retries = 0
        text2check = "you are human"
        if not self.check_visibility(text2check):
            print("No captcha detected")
            return True
        while self.check_visibility(text2check) and retries < self.max_retries:
            retries += 1
            self.driver.sleep(1)
            self.driver.uc_gui_click_captcha()
        self.driver.sleep(4)
        return not self.check_visibility(text2check)
