# SortPipe: automatic pipeline from kilosort to plexon offline sorter

## Directory structure:

Requires to put a config file (sortpipe_config.csv) in a directory named "config".

sortpipe (this repository)\
-- mainfunc\
-- lib\
config\
-- sortpipe_config.csv

## Example config file (sortpipe_config.csv):

sample_rate, 30000\
n_electrodes, 32\
kilo_sorted_dir, ../../data/kiloSorted_Nana32\
plexon_input_dir, ../../data/toPlexonOfflineSorter_Nana32\
manually_sorted_dir, ../../data/toPlexonOfflineSorter_Nana32\
for_stability_analysis_dir, ../../data/forStabilityAnalysis_Nana32