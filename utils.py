# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:16:27 2021

@author: Fatemeh
"""

import pandas as pd
import numpy as np
import matplotlib


def remove_nans(list_1, list_2):
    """remove every corresponding element in list_2 that has nan value in list_1"""
    nans = np.isnan(list_1)
    nan_indecis = np.where(nans)[0]
    return np.delete(list_2, nan_indecis).tolist()


def read_meta(metadata, id_name):
    print("reading metadata...")
    tsv_read = pd.read_csv(metadata, sep='\t')
    metadata_info = tsv_read[[id_name, 'date', 'date_submitted']]
    metadata_info = metadata_info.set_index(id_name)
    return metadata_info


def date_to_num(X):
    """convert a list of datetime dates to a list of numbers with order"""
    Xnew = matplotlib.dates.date2num(X)
    return Xnew


def remove_non_val_dates(dates):
    """removes no valid dates from the list of string dates with format 0000-00-00"""
    valid_dates = []
    for date in dates:
        if len(date) == 10:
            try:
                valid = np.datetime64(date)
                valid_dates.append(date)
            except:
                continue
    return valid_dates


def generate_datapoints(dates, mode, time_period, start_delay):
    """from the start date (+ start_delay), it calculates all the dates 'time_period' number of days apart from 
    each other, and converts it to a list of numbers if it is datetime"""
    dates = np.sort(dates)
    start = dates[0]
    end = dates[len(dates)-1]
    timepoints = []
    if (mode == 'date'):
        date = start + np.timedelta64(start_delay,'D')
    else:
        date = start + start_delay
    timepoints.append(start)
    while True:
        if (mode == 'date'):
            date =  date + np.timedelta64(time_period,'D')
        else:
            date = date + time_period
        timepoints.append(date)
        if(date >= end):
            break
    try:
        timepoints = date_to_num(timepoints)
    except:
        pass
    return timepoints