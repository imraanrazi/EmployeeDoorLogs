from pickle import TRUE
from sqlite3 import Timestamp
from numpy import true_divide
import pandas as pd
import datetime
from datetime import date, time, timedelta
import os
from os import path
import shutil
import glob
import sys
import json
import smtplib
from getpass import getpass
from email.mime.text import MIMEText
from os import listdir
import time
import sched, time



s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
   while True:

    def find_csv_filenames( path_to_dir, suffix=".csv" ):
        filenames = listdir(path_to_dir)
        return [ filename for filename in filenames if filename.endswith( suffix ) ]
 

    def initialize_access_log_table(df_Table):

        return df_Table

     

    # define function that will sort the rows of a given table in ascending order by given column name

    def datCnv(src):
        return pd.to_datetime(src)

    def order_by_time(df_ToOrder, field_name):

        df_ToOrder['Timestamp']=df_ToOrder['Timestamp'].astype(str)
        df_ToOrder['format'] = 1
        df_ToOrder.loc[df_ToOrder.Timestamp.str.contains('/'), 'format'] = 2
        df_ToOrder['Timestamp'] = pd.to_datetime(df_ToOrder.Timestamp)

        # Convert to datetime with two different format settingsh  
        df_ToOrder.loc[df_ToOrder.format == 1, 'Timestamp'] = pd.to_datetime(df_ToOrder.loc[df_ToOrder.format == 1, 'Timestamp'], format = '%d-%m-%Y %H:%M:%S')
        df_ToOrder.loc[df_ToOrder.format == 2, 'Timestamp'] = pd.to_datetime(df_ToOrder.loc[df_ToOrder.format == 2, 'Timestamp'], format = '%d/%m/%Y %H:%M:%S')

        df_ToOrder = df_ToOrder.loc[~df_ToOrder.Timestamp.isnull()]


        df_ToOrder.sort_values(field_name, axis=0, ascending=True,

                               inplace=True, na_position='last')
        return df_ToOrder
     

    def assign_shift(df_ToAssignShift, dsStart, dsEnd, nsStart, nsEnd):

        for j in range(1, len(df_ToAssignShift)):

            ts_str = df_ToAssignShift.at[j, 'Timestamp']
            ts_str1 = ts_str.strftime("%H:%M:%S")

     

            if (ts_str1 >= dsStart) and (ts_str1 < dsEnd):
                df_ToAssignShift.at[j, 'Shift'] = "Day"

            else:

                df_ToAssignShift.at[j, 'Shift'] = "Night"
        return df_ToAssignShift

             

    # Open config file and load configuration in dictionsary

    configFile = open('config.json')

    config = json.load(configFile)

    ################################################################################

    ############### Setup and Initialize the main datafram table ###################

    ################################################################################

    # Read in the raw csv file from folder into a dataframe container, then remove

    # the first column which is a blank and the 6th column that are pictures

    # df_original = pd.read_csv('AccessLogConversion\\dooractivities.csv')

    # If the file does not exist exit the code

    try:

        df_original = pd.read_csv("Z:\\dooractivities.csv")

    except:

        print("File not found!")

        sys.exit()

     

    # Create a header for the table

    df_original.columns = ['Manway', 'Access Point', 'First Name',

                           'Last Name', 'Timestamp', 'Company', 'Structure', 'Card ID', 'Craft']

     

    # Delete the first row of the table then copy the table into a new dataframe container

    df_formatted = df_original.drop(labels=range(0, 1), axis=0)

     
    # Add new columns to the table

    df_formatted['Exit Timestamp'] = None
    df_formatted['HCValue'] = None
    df_formatted['TripID'] = None
    df_formatted['Shift'] = None


    # Initialize the HCValue and TripID columns

    df_formatted.loc[:, 'HCValue'] = 0
    df_formatted.loc[:, 'TripID'] = 0


    # Order the rows chronologically

    df_formatted = order_by_time(df_formatted, "Timestamp")


    # Establish key shift time values

    dayShiftStartTime = config["dayShiftStartTime"]
    dayShiftEndTime = config["dayShiftEndTime"]
    nightShiftStartTime = config["nightShiftStartTime"]
    nightShiftEndTime = config["nightShiftEndTime"]
    df_formatted = assign_shift(df_formatted, dayShiftStartTime, dayShiftEndTime, nightShiftStartTime, nightShiftEndTime)

     

    ############## Main program variables initialization ############
    # tripCounter will keep track of paired INs and OUTs in the  Access Point Column

    tripCounter = 0                 # This keeps the track of the total number of trips

    df_length = len(df_formatted)   # assign length of main table to a variable

     

    # This is the main loop. Find each Reader - In row in this chronologically sorted table, and then find it's associated Reader - Out

    for i in range(0, df_length):
        if (df_formatted.at[df_formatted.index[i], 'Access Point'] == "Reader - In"):
            rowIndexToCheck = i+1
            exitEventFound = False
            while ((not (exitEventFound)) and (df_length > rowIndexToCheck)):

                if (df_formatted.at[df_formatted.index[rowIndexToCheck], 'Access Point'] == "Reader - Out"):

                    # print("In Reader - Out check ")

                    if (df_formatted.at[df_formatted.index[rowIndexToCheck], 'TripID'] == 0):

                        # print("In TripID check ")

                        if (df_formatted.at[df_formatted.index[rowIndexToCheck], 'Card ID'] == df_formatted.at[df_formatted.index[i], 'Card ID']):

                            if (df_formatted.at[df_formatted.index[rowIndexToCheck], 'Structure'] == df_formatted.at[df_formatted.index[i], 'Structure']):

                                if (df_formatted.at[df_formatted.index[rowIndexToCheck], 'Shift'] == df_formatted.at[df_formatted.index[i], 'Shift']):

                                    time_difference = df_formatted.at[df_formatted.index[rowIndexToCheck],'Timestamp'] - df_formatted.at[df_formatted.index[i], 'Timestamp']

                                    if (time_difference) < timedelta(hours=12):

                                        exitEventFound = True

                                        tripCounter += 1

                                        df_formatted.at[df_formatted.index[i],
                                                        'TripID'] = tripCounter
                                                        
                                        df_formatted.at[df_formatted.index[rowIndexToCheck],

                                                        'TripID'] = tripCounter

                                        df_formatted.at[df_formatted.index[i],

                                                        'HCValue'] = 1

                                        df_formatted.at[df_formatted.index[rowIndexToCheck],

                                                        'HCValue'] = -1

                                        df_formatted.at[df_formatted.index[i],

                                                        'Exit Timestamp'] = df_formatted.at[df_formatted.index[rowIndexToCheck], 'Timestamp']

                rowIndexToCheck += 1

     
    # Capture the current time in the format shown
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    # Name the file that we will save the dataframe to
    file_name = "ModifiedDooractivities" + now + ".csv"

    # If the value is true to remove the four columns, remove them and update the dataframe
    if config['RemoveFourColumns'].lower() == 'true':

        df_formatted = df_formatted.iloc[:, :-4]

    # Export the dataframe to the file
    df_formatted.to_csv(file_name)
    upload_file_list = [file_name]

    try:
        with open("Z:\\dooractivities.csv") as file:
            try:
                read_data = file.read()
            except:
                print("File opened")
    except:
        print("Could not open file")

     

    # Used too move the new .csv file to the correct folder

    source_dir = r'Z:'
    dest_dir = r'C:\Users\General\Desktop\genetecfolder'
    files = glob.iglob(os.path.join(source_dir, "*.csv"))


    # Check if there are csv files in the destination directory

    if files:
        for file in files:
            if os.path.isfile(file):
                shutil.move(file, dest_dir)
    else:
        print("No files present in source folder")


    try:
    #Used to send the original file to the Archive Folder
        os.replace(r"C:\Users\General\Desktop\genetecfolder\dooractivities.csv", r"C:\Users\General\Desktop\sharedfolder\dooractivities.csv")
        print("Original Excel file has been moved to the Archivelog folder")
    except:
        print("Error Excel file not found, please upload an excel file to the Shared Folder")

s.enter(60, 1, do_something, (s,))
s.run()