from dotenv import load_dotenv
from Emailer import *
import os, json

def create_reminder(instruction):
    check_symbol = "-"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, instruction)

def create_step(reminder):
    check_symbol = "☐"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, reminder)

def get_header(name, date_maintenance):
    header = "Hi {},\n\nThis is a reminder that tomorrow ({}) is your turn to do the LFL Lab Maintenance. Please refer to the following checklist.\n\n".format(name, date_maintenance)
    return header

def get_signature(bot_name="LFL Bot"):
    salute = "🫡 "
    # salute = ""
    return "\n\nThank you for your service {},\n{}".format(salute, bot_name)

def get_reminders(reminders_list):
    reminders = []
    for reminder_string in reminders_list:
        reminders.append(create_reminder(reminder_string))
    prompt = "\n\nSome safety considerations from EH&S:\n"
    reminders = "".join(reminders)
    return prompt + reminders + "\n"


def create_email_content(name, date_maintenance, instructions, reminders, bot_name="LFL Bot"):
    header = get_header(name, date_maintenance)
    steps = []
    for instruction in instructions:
        steps.append(create_step(instruction))
    body = "".join(steps)
    reminders = get_reminders(reminders)
    signature = get_signature(bot_name)
    return header + body + reminders + signature

def extract_lab_maintainer():
    load_dotenv(".env")
    user_id = str(os.environ.get("USER_ID"))
    user_name, user_email = get_user_info(user_id)
    return user_name, user_email

def get_user_info(user_id):
    f = open("lab_members.json")
    data = json.load(f)
    user_name, user_email = data[user_id]["name"], data[user_id]["email"]
    return user_name, user_email

def get_last_user_id():
    f = open("lab_members.json")
    data = json.load(f)
    id_num = int(list(data.keys())[-1])
    return id_num

def send_email(email,subjectLine, emailContent):
    sms_list = ['']
    sender = Emailer(email, sms_list, subjectLine, emailContent)
    sender.send_email()

def update_record(f=".env"):
    # Read in the file
    load_dotenv(f)
    last_id = get_last_user_id()

    with open(f, 'r') as file :
        filedata = file.read()

    # Replace the target string
    user_id = int(os.environ.get("USER_ID"))
    target = "ID="+str(user_id)

    if user_id != last_id:
        update = "ID="+str(user_id+1)
    else:
        update = "ID="+str(1)

    filedata = filedata.replace(target, update)

    # Write the file out again
    with open(f, 'w') as file:
        file.write(filedata)
