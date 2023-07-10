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

from HelperFunctions import *
from datetime import datetime, timedelta

if __name__ == "__main__":
    # weekday choice (day in advance)
    #date_maintenance = str(datetime.date.today() + datetime.timedelta(days=1))
    
    # Get today's date
    date_maintenance = datetime.today().date()

    # Get the date five days from today
    end_date = date_maintenance + timedelta(days=5)

    # Convert dates to strings
    start_date_str = str(date_maintenance)
    end_date_str = str(end_date)

    # liquid nitrogen appt time
    ln2time = "15:00"
    
    # Define the event details
    location = "LFL Lab"

    # content of email
    ln2_instruction = "Please schedule a Liquid Nitrogen Fill Up with Jivin (jseward@usc.edu) and refill our tank"

    instructions = [ln2_instruction, "Check Lab Inventory: napkins, water filters, gloves, masks, printing supply, compressed air", "Check Chemical Inventory", "Assess Water Filter Status", "Check cooling water temperature and pressure", "Fill up traps and dewars with LN2", "General Cleanup of the Lab (call people out if needed)","Monitor waste labels and complete them if they are missing any information", "Issue a Waste Pick Up Request with EH&S if Accumulation Date on a label is almost 9 months or if you need to dispose of the waste ASAP", "Version Control and Back Up Code Base on GitHub"]
    reminders = ["🌳 Wear O2 monitor while doing LN2 fill up","🚪 Keep Back Room Door open while doing LN2 fill up","🪤 Don't position yourself such that you are trapped by the dewar","👖 Wear full pants on Lab Maintenance Day", "🚫 Don't reuse gloves", "🦠 Don't touch non-contaminated items with gloves", "🧤 Wear thermal gloves when working with LN2", "🥼🥽 Wear safety coat and goggles", "👥 Use the buddy system if not comfortable doing a task alone"]

    """
    Logic:
    """

    # read emission file to see whose turn this week (i.e. at execution)
    recipient_name, recipient_email = extract_lab_maintainer()

    # create email for lab maintainer
    email_content = create_email_content(recipient_name, date_maintenance, instructions, reminders)
    subjectLine = "LFL Lab Maintenance Reminder ({})".format(date_maintenance)

    # Create the event
    event_link = create_event_with_dates(subjectLine, location, email_content, start_date_str, end_date_str)

    # send email to lab maintainer
    send_email(recipient_email, subjectLine, email_content)

    # update the record
    update_record()
