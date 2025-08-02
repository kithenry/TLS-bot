#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta


def read_json(fname, encoding="utf-8"):
    try:
        with open(fname, mode="r", encoding=encoding) as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        print(f"File {fname} not found")
        return []


def write_json(fname, dump_data, encoding="utf-8"):
    try:
        with open(fname, mode="w", encoding=encoding) as write_file:
            json.dump(dump_data, write_file, indent=4, ensure_ascii=False)
            print(f"Data written to: {fname}")
    except Exception as e:
        print(f"Error writing to {fname}: {e}")


def write_generic(fname, write_data):
    try:
        with open(fname, "w") as f:
            f.write(write_data)
            print(f"Data written to {fname}")
    except Exception as e:
        print(f"Error writing to {fname}: {e}")


def manage_profile_attempts(profile_dir, max_attempts, expiry_hours):
    attempt_file = f"{profile_dir}/attempts.json"
    now = datetime.now()
    if os.path.exists(attempt_file):
        data = read_json(attempt_file)
        attempts = data.get("attempts", 0)
        last_reset = datetime.fromisoformat(data.get("last_reset", now.isoformat()))
        if now - last_reset > timedelta(hours=expiry_hours):
            attempts = 0
            last_reset = now
    else:
        attempts = 0
        last_reset = now

    attempts += 1
    write_json(
        attempt_file, {"attempts": attempts, "last_reset": last_reset.isoformat()}
    )
    return attempts <= max_attempts
