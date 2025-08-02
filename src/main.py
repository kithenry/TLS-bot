#!/usr/bin/env python3

import time
import random
from seleniumbase import Driver
from modules.captcha import CaptchaSolver
from modules.navigation import Navigation
from modules.login import Login
from modules.appointment import Appointment
from modules.safe_clicker import SafeClick
from modules.messaging import Messaging
from multiprocessing import Process, cpu_count
from utils import file_io


def load_config():
    config = file_io.read_json("config.json")
    accounts = file_io.read_json(config["accounts_file"])
    config["accounts"] = accounts
    return config


def check_account(email, password, config, profile_dir):
    driver = Driver(uc=True, user_data_dir=profile_dir)
    try:
        clicker = SafeClick(driver)
        captcha_solver = CaptchaSolver(driver, config["max_retries"])
        navigation = Navigation(driver, config["center"], captcha_solver, clicker)
        login = Login(driver, captcha_solver, clicker)
        appointment = Appointment(driver, captcha_solver, clicker)
        messaging = Messaging(config["telegram_token"], config["telegram_chat_id"])

        print(f"Checking account: {email}")
        driver.uc_open_with_reconnect(config["tls_url"], 2)
        navigation.page_refresher()
        captcha_solver.solve()
        print("navigating prelogin")
        navigation.navigate_pre_login()
        navigation.select_center()
        [wasAlreadyIn, failedLogin] = login.login(email, password)
        if not failedLogin:
            if not wasAlreadyIn:
                try:
                    # check if redirected to prelogin .. else, go direct to view group sequence
                    if navigation.back_to_prelogin():
                        print("Redirected to pre-login, re-running sequence")
                        navigation.navigate_pre_login()
                        captcha_solver.solve()
                        navigation.select_center()
                        captcha_solver.solve()
                    # need logic to halt ops while captcha is being solved
                except Exception as e:
                    file_io.write_generic("pre_loginpage.html", driver.page_source)
                    print("Failed to navigate prelogin, ", e)
                    driver.quit()

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
            print("Login failed")
            driver.quit()
    except Exception as e:
        print("Uncaught exception", e)
        driver.quit()


def worker(account, config):
    profile_dir = f"assets/profiles/chrome_profile_{account['email'].replace('@', '_')}"
    attempts = file_io.manage_profile_attempts(
        profile_dir, config["max_attempts_per_profile"], config["profile_expiry_hours"]
    )
    if not attempts:
        print(f"Profile for {account['email']} expired, clearing...")
        # Clear profile logic goes here
    check_account(account["email"], account["password"], config, profile_dir)


def main():
    config = load_config()
    accounts = config["accounts"]
    if not accounts:
        print("No accounts found in customers.json")
        return
    # for testing
    # accounts = [accounts[0]]
    total_cores = cpu_count()
    max_parallel = max(1, int(total_cores * 0.6))
    to_use = min(max_parallel, config["max_procs"])
    print(f"Detected {total_cores} cores, using up to {to_use} in parallel")

    running_processes = []
    account_queue = accounts.copy()

    while account_queue or running_processes:
        # Clean up finished processes
        still_running = []
        for proc in running_processes:
            if proc.is_alive():
                still_running.append(proc)
            else:
                proc.join()
        running_processes = still_running

        # Start new processes if under limit
        while account_queue and len(running_processes) < to_use:
            account = account_queue.pop(0)
            p = Process(target=worker, args=(account, config))
            p.start()
            running_processes.append(p)
            time.sleep(0.5)

        time.sleep(1)  # Avoid tight loop when waiting


if __name__ == "__main__":
    main()
