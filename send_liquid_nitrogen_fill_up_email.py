# -*- coding: utf-8 -*-
"""
===================================================================
Program : LFL_Lab_Maintenance/liquid_nitrogen_fill_up_email.py
===================================================================
Summary:
    0) choose compatible time with Megan and everyone
    1) remind lab maintainer about liquid nitrogen fill up time
    - works with a daemon/cron controller for execution
"""
__author__ =  "Sadman Ahmed Shanto"
__date__ = "07/18/2022"
__email__ = "shanto@usc.edu"

# read emission file to see whose turn this week (i.e. at execution)
recipient = ""

# update emission file with new person's turn
