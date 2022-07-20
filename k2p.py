import hdf5storage
import numpy as np
from mainfunc.converter import convert
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

params = read_config()

for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.plexon_input_dir, 'mat'):
    print('subsession_path =', subsession_path)
    sessionID = subsession_path.split('/')[0]
    make_directories(params.plexon_input_dir, subsession_path)
    in_path = params.kilo_sorted_dir + '/' + subsession_path
    out_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    converted = convert(in_path, np.double(params.sample_rate), int(params.n_electrodes))
    hdf5storage.savemat(out_path, converted, format='7.3', oned_as='column')