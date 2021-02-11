# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 19:08:55 2021

@author: Fatemeh
"""

import pandas as pd
import numpy as np
import os, sys
from utils import generate_datapoints, date_to_num, read_meta, remove_non_val_dates

    
def calculate_sum_per_timepoints(list_, dates, timepoints):
    """calculates the sum of elements in the list_ for all dates between timepoints, where dates and timepoints are
    numbers (date_to_num() results)"""
    last_timepoint = timepoints[0] - 1 
    summation_list = []
    for timepoint in timepoints[1:]:
        indices = np.where((last_timepoint < dates) & (dates <= timepoint))[0]
        last_timepoint = timepoint
        if indices.size == 0:
            summation_list.append(np.nan)
        else:
            summation_list.append(np.sum(np.array(list_)[indices]))
    return summation_list


def get_counts_for_cluster(cluster_counts, cluster):
    """extracts the count for a specific cluster for all tuples (each day has a tuple) in cluster_counts and
    returns it as a list"""
    counts = []
    for i in range(len(cluster_counts)):
        try:
            counts.append([item[1] for item in cluster_counts[i] if str(item[0]) == cluster][0])
        except:
            counts.append(0) 
    return counts


def calculte_frequency(cluster_counts, dates, clusters, time_period, start_delay):
    """reads the data out of the csv file and returns the frequencies as dataframes, rows are weeks and columns are 
    clusters' frequency"""
    dates = pd.to_datetime(dates)
    weeks_indices = generate_datapoints(dates, 'date', time_period, start_delay)
    dates_indices = date_to_num(dates)

    cluster_freq = pd.DataFrame()
    
    for cluster in clusters:
        frequencies = get_counts_for_cluster(cluster_counts, str(cluster))
        weekly_cluster_freq = calculate_sum_per_timepoints(frequencies, dates_indices, weeks_indices)
        cluster_freq[str(cluster)] = weekly_cluster_freq
    cluster_freq.index = weeks_indices[1:]
    return cluster_freq


def find_daily_counts(metadata_info, all_submission_dates, label_name, file):
    """find counts of members of each cluster for each date"""
    df = pd.DataFrame()
    dates = []
    daily_cluster_counts = []
    for date in all_submission_dates:
        df = metadata_info.groupby('date').get_group(date)
        count = df.groupby(label_name).count()
        dates.append(date)
        daily_cluster_counts.append(list(zip(list(count.index), list(count['date'].values))))
    dates, daily_cluster_counts = zip(*list(sorted(zip(dates, daily_cluster_counts))))
    return dates, daily_cluster_counts



def clusters_counts(labels_file, metadata_file, id_):
    """matches ids in labeling file and metadata file to find the submission date for each id, 
    then returns the daily counts of each cluster"""
    labels = pd.read_csv(labels_file)
    labels = labels.set_index(labels.columns[0])
    label_name = labels.columns[0]
    clusters_name = labels[label_name].unique()
    metadata_info = read_meta(metadata_file, id_) 

    ixs = metadata_info.index.intersection(labels.index)
    # print(ixs)
    metadata_info = metadata_info.loc[ixs]
    labels = labels.loc[ixs]
    all_submission_dates = remove_non_val_dates(metadata_info['date'].unique())
    metadata_info[label_name] = labels.values
    return clusters_name, find_daily_counts(metadata_info, all_submission_dates, label_name, labels_file)
    


if __name__ == '__main__':
    labels_file = sys.argv[1]
    metadata_file = sys.argv[2]
    time_period = sys.argv[3]
    delay = sys.argv[4]
    #here id_name can be 'gisaid_epi_isl' or 'strain'
    id_name = sys.argv[5]
    clusters_name, [dates, counts] = clusters_counts(labels_file, metadata_file, id_name)
    frequency = calculte_frequency(counts, dates, clusters_name, time_period, delay)
    frequency.to_csv(labels_file.split(".csv")[0] + "_clusters_freq.csv")
