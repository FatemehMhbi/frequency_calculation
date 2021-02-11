# frequency_calculation
This code reads a labeling file which includes some sequences' ids and their labels (dividing sequences into different groups or clusters) and a metadata file. The metadata file which is in .tsv format includs submission dates for the sequences. Then it calculates the frequency or the counts of memebrs of each cluster through time. It saves the frequencies as a csv file, where the index of each row is the time (matplotlib.dates.date2num()), and columns are clusters.

# How to run:
python3.7 frequency_from_labeling.py labeling_file.csv metadata.tsv time_period delay id_name 

time_period: the period as number of the days that we want the frequency to be reported. For example if time_period = 7 then weekly counts are reported. \
delay: a number. If zero, the first date that the first sequences were submitted is the starting date for frequency report (start date = first submission date + delay) \
id_name: the name of id to match the sequences in metadata file and the labeling file for example it can be 'strain' or 'gisaid_epi_isl'. \
The output is saved as 'labeling_file_clusters_freq.csv'.
