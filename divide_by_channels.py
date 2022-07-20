import numpy as np
import hdf5storage
from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

for subsession_path in get_unprocessed(params.plexon_input_dir, params.for_stability_analysis_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    trg_dir = params.for_stability_analysis_dir + '/' + sessionID + '/elc_01plx'
    make_directories(trg_dir)

    # orig_data = hdf5storage.loadmat(orig_path, format='7.3', oned_as='column')
    orig_data = hdf5storage.loadmat(src_path)
    wvf = orig_data['wvf']
    times = orig_data['times']

    for orig_electrodeID in range(len(wvf)):

        wvf_single_cell = wvf[orig_electrodeID]
        times_single_cell = times[orig_electrodeID]
        divided = dict(wvf=wvf_single_cell, times=times_single_cell)
        new_electrodeID = str(orig_electrodeID + 1)
        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '.mat'
        trg_path = trg_dir + '/' + trg_fileName
        hdf5storage.savemat(trg_path, divided, format='7.3', oned_as='column')
