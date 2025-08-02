#!/usr/bin/env python3

import threading
import time
import random
from seleniumbase import Driver
from modules.captcha import CaptchaSolver
from modules.navigation import Navigation
from modules.login import Login
from modules.appointment import Appointment
from modules.messaging import Messaging
from utils import file_io


def load_config():
    config = file_io.read_json("config.json")
    print(config)
    accounts = file_io.read_json(config["accounts_file"])
    config["accounts"] = accounts
    return config


def check_account(email, password, config, profile_dir):
    driver = Driver(uc=True, user_data_dir=profile_dir)
    try:
        captcha_solver = CaptchaSolver(driver, config["max_retries"])
        navigation = Navigation(driver, config["center"], captcha_solver)
        login = Login(driver, captcha_solver)
        appointment = Appointment(driver, captcha_solver)
        messaging = Messaging(config["telegram_token"], config["telegram_chat_id"])

        print(f"Checking account: {email}")
        driver.uc_open_with_reconnect(config["tls_url"], 2)
        navigation.page_refresher()
        captcha_solver.solve()
        navigation.navigate_pre_login()
        navigation.select_center()
        [wasAlreadyIn, loginFailed] = login.login(email, password)
        if not loginFailed:
            if not wasAlreadyIn:
                try:
                    print("Redirected to pre-login, re-running sequence")
                    navigation.navigate_pre_login()
                    navigation.select_center()
                    appointment.go_to_group_page()
                except Exception as e:
                    # its the application page, no need to do prelogin
                    print("Failed to do prelogin proc: ", e)
                    file_io.write_generic("pre_loginpage.html", driver.page_source)
            elif wasAlreadyIn:
                appointment.go_to_group_page()
                appointment.view_group()
            if appointment.check_availability():
                messaging.send_message(f"Appointment available for {email}!")
            else:
                messaging.send_message(f"No appointment available for {email}")
                time.sleep(
                    random.uniform(
                        config["check_interval_min"], config["check_interval_max"]
                    )
                )
        else:
            print("Failed to login")
    finally:
        driver.quit()


def worker(account, config):
    profile_dir = f"assets/profiles/chrome_profile_{account['email'].replace('@', '_')}"
    attempts = file_io.manage_profile_attempts(
        profile_dir, config["max_attempts_per_profile"], config["profile_expiry_hours"]
    )
    if not attempts:
        print(f"Profile for {account['email']} expired, clearing...")
        # Clear profile (implement profile clearing logic if needed)
        return
    check_account(account["email"], account["password"], config, profile_dir)


def main():
    config = load_config()
    accounts = config["accounts"]
    if not accounts:
        print(f"No accounts found in {accounts['accounts_file']}")
        return

    threads = []
    for account in accounts:
        if len(threads) >= config["max_threads"]:
            for t in threads:
                t.join()
            threads = []
        t = threading.Thread(target=worker, args=(account, config))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
