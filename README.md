# SortPipe: automatic pipeline from kilosort to plexon offline sorter

## Directory structure:

Requires to put a config file (sortpipe_config.csv) in a directory named "config".

sortpipe (this repository)\
-- mainfunc\
-- lib\
config\
-- softpipe_config.csv\

## Example config file (sortpipe_config.csv):

sample_rate, 30000\
n_electrodes, 32\
kilo_sorted_dir, ../../kiloSorted\
plexon_input_dir, ../../plexonSorterInput\
output_mat_file_name, k2p.mat
