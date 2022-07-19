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
    ln2_instruction = "Liquid Nitrogen Fill Up with Megan @ {}".format(ln2time)
    instructions = [ln2_instruction, "Check Lab Inventory: napkins, water filters, gloves, masks, printing supply, compressed air", "Check Chemical Inventory", "Assess Water Filter Status", "Check cooling water temperature and pressure", "Fill up traps and dewars with LN2", "General Cleanup of the Lab (call people out if needed)"]

    """
    Logic:
    """
    # read emission file to see whose turn this week (i.e. at execution)
    recipient_name, recipient_email = extract_lab_maintainer()

    # create email for lab maintainer
    email_content = create_email_content(recipient_name, date_maintenance, instructions)
    subjectLine = "LFL Lab Maintenance Reminder ({})".format(date_maintenance)

    # send email to lab maintainer
    send_email(recipient_email, subjectLine, email_content)

    # update the record
    update_record()
