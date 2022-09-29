# -*- coding: utf-8 -*-
"""
==================================================================
Program : LFL_Lab_Maintenance/start_lab_maintenance_alerts.py
==================================================================
Summary:
    - will choose whose turn it is and send them an email
    - works with a daemon/cron controller for execution
"""
__author__ =  "Sadman Ahmed Shanto"
__date__ = "07/18/2022"
__email__ = "shanto@usc.edu"

import datetime
from HelperFunctions import *

if __name__ == "__main__":
    # weekday choice (day in advance)
    date_maintenance = str(datetime.date.today() + datetime.timedelta(days=1))

    # liquid nitrogen appt time
    ln2time = "3 PM"

    # content of email
    ln2_instruction = "Please schedule a Liquid Nitrogen Fill Up with Megan (+1293090882) and refill our tank"
    #instructions = [ln2_instruction, "Check Lab Inventory: napkins, water filters, gloves, masks, printing supply, compressed air", "Check Chemical Inventory", "Assess Water Filter Status", "Check cooling water temperature and pressure", "Fill up traps and dewars with LN2", "General Cleanup of the Lab (call people out if needed)","Monitor waste labels and complete them if they are missing any information", "Issue a Waste Pick Up Request with EH&S if Accumulation Date on a label is almost 9 months or if you need to dispose of the waste ASAP"]
    #reminders = ["Wear O2 monitor while doing LN2 fill up","Keep Back Room Door open while doing LN2 fill up","Don't position yourself such that you are trapped by the dewar","👖 Wear full pants on Lab Maintenance Day", "🚫 Don't reuse gloves", "🦠 Don't touch non-contaminated items with gloves", "🧤 Wear thermal gloves when working with LN2", "🥼🥽 Wear safety coat and goggles", "👥 Use the buddy system if not comfortable doing a task alone"]

    instructions = [ln2_instruction, “Check Lab Inventory: napkins, water filters, gloves, masks, printing supply, compressed air”, “Check Chemical Inventory”, “Assess Water Filter Status”, “Check cooling water temperature and pressure”, “Fill up traps and dewars with LN2”, “General Cleanup of the Lab (call people out if needed)“,”Monitor waste labels and complete them if they are missing any information”, “Issue a Waste Pick Up Request with EH&S if Accumulation Date on a label is almost 9 months or if you need to dispose of the waste ASAP”, “Version Control and Back Up Code Base on GitHub”]
    reminders = [“:deciduous_tree: Wear O2 monitor while doing LN2 fill up”,“:door: Keep Back Room Door open while doing LN2 fill up”,“:mouse_trap: Don’t position yourself such that you are trapped by the dewar”,“:jeans: Wear full pants on Lab Maintenance Day”, “:no_entry_sign: Don’t reuse gloves”, “:microbe: Don’t touch non-contaminated items with gloves”, “:gloves: Wear thermal gloves when working with LN2”, “:lab_coat::goggles: Wear safety coat and goggles”, “:busts_in_silhouette: Use the buddy system if not comfortable doing a task alone”]

    """
    Logic:
    """
    # read emission file to see whose turn this week (i.e. at execution)
    recipient_name, recipient_email = extract_lab_maintainer()

    # create email for lab maintainer
    email_content = create_email_content(recipient_name, date_maintenance, instructions, reminders)
    subjectLine = "LFL Lab Maintenance Reminder ({})".format(date_maintenance)

    # send email to lab maintainer
    send_email(recipient_email, subjectLine, email_content)

    # update the record
    update_record()
