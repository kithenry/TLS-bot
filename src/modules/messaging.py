#!/usr/bin/env python3

import requests
import json


class Messaging:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Telegram message sent successfully")
            else:
                print(f"Failed to send Telegram message: {response.text}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
