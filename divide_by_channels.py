import numpy as np
from scipy.io import savemat as scipy_savemat
from scipy.io import loadmat as scipy_loadmat
from scipy.io.matlab.miobase import MatReadError, MatWriteError
from hdf5storage import savemat as hdf5_savemat
from hdf5storage import loadmat as hdf5_loadmat

from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

for subsession_path in get_unprocessed(params.plexon_input_dir, params.for_stability_analysis_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    trg_dir = params.for_stability_analysis_dir + '/' + sessionID + '/elc_01plx'
    make_directories(trg_dir)

    try:
        orig_data = scipy_loadmat(src_path)
    except MatReadError:
        orig_data = hdf5_loadmat(src_path)
    wvf = orig_data['wvf']
    times = orig_data['times']

    for orig_electrodeID in range(len(wvf)):

        wvf_1by1 = np.array([wvf[orig_electrodeID]], dtype=object)
        times_1by1 = np.array([times[orig_electrodeID]], dtype=object)
        divided = dict(wvf=wvf_1by1, times=times_1by1)
        new_electrodeID = str(orig_electrodeID + 1)
        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '.mat'
        trg_path = trg_dir + '/' + trg_fileName
        try:
            scipy_savemat(trg_path, divided)
        except MatWriteError:
            hdf5_savemat(trg_path, divided, format='7.3', oned_as='column')
        