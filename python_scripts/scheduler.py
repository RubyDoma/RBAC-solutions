import subprocess
import time

import schedule

script1 = "python_scripts/trigger_terraform_if_change_in_user_info.py"
script2 = "python_scripts/trigger_terraform_if_change_in_roles.py"
script3 = "python_scripts/trigger_terraform_if_change_in_permissions.py"


def trigger_terraform_if_user_info_changed():
    subprocess.run(["python", script1])


def trigger_terraform_if_roles_changed():
    subprocess.run(["python", script2])


def trigger_terraform_if_permissions_changed():
    subprocess.run(["python", script3])


# Schedule script to run every day at 2:30 PM
schedule.every().day.at("14:30").do(trigger_terraform_if_user_info_changed)
schedule.every().day.at("14:30").do(trigger_terraform_if_roles_changed)

# Schedule script to run every hour
schedule.every().hour.do(trigger_terraform_if_permissions_changed)

while True:
    schedule.run_pending()
    time.sleep(1)
