import numpy as np
from scipy.io import savemat
from mainfunc.converter import convert
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

params = read_config()
sep = params.sep
for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.plexon_input_dir, params.output_mat_file_name, sep):
    print('subsession_path =', subsession_path)        
    make_directories(params.plexon_input_dir, subsession_path, sep)    
    in_path = params.kilo_sorted_dir + sep + subsession_path
    out_path = params.plexon_input_dir + sep + subsession_path + sep + params.output_mat_file_name
    savemat(out_path, convert(in_path, np.double(params.sample_rate), int(params.n_electrodes), sep))
