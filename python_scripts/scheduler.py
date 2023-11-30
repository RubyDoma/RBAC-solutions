import subprocess
import time

import schedule


def trigger_terraform_if_user_info_changed():
    subprocess.run(["python", "trigger_terraform_if_change_in_user_info.py"])


def trigger_terraform_if_roles_changed():
    subprocess.run(["python", "trigger_terraform_if_change_in_roles.py"])


def trigger_terraform_if_permissions_changed():
    subprocess.run(["python", "trigger_terraform_if_change_in_permissions.py"])


# Schedule script to run every day at 2:30 PM
schedule.every().day.at("14:30").do(trigger_terraform_if_user_info_changed)
schedule.every().day.at("14:30").do(trigger_terraform_if_roles_changed)

# Schedule script to run every hour
schedule.every().hour.do(trigger_terraform_if_permissions_changed)

while True:
    schedule.run_pending()
    time.sleep(1)
