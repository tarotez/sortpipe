from os import listdir
from scipy.io import savemat
from mainfunc.converter import convert
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

sep = "/"
params = read_config()
for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.plexon_input_dir, sep):
    print('subsession_path =', subsession_path)        
    make_directories(params.plexon_input_dir, subsession_path, sep)    
    in_path = params.kilo_sorted_dir + sep + subsession_path
    out_path = params.plexon_input_dir + sep + subsession_path + '/k2p.mat'    
    savemat(out_path, convert(in_path, params.sample_rate, params.n_electrodes))    
