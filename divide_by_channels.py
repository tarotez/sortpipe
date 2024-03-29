import numpy as np
# from hdf5storage import savemat as hdf5_savemat
from scipy.io import savemat as scipy_savemat
from hdf5storage import loadmat as hdf5_loadmat

from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

for subsession_path in get_unprocessed(params.plexon_input_dir, params.matrix_not_cell_array_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    subsessionID_without_s = subsessionID[1:]
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    trg_dir = params.matrix_not_cell_array_dir + '/' + sessionID + '/elc_01plx'
    make_directories(trg_dir)

    converted = hdf5_loadmat(src_path)
    wvf_byc = converted['wvf']
    times_byc = converted['times']
    # print('times.shape =', times.shape)

    for orig_electrodeID in range(len(wvf_byc)):
        # print('times.shape =', times[orig_electrodeID].shape)
        
        # print('wvf_byc[0].shape =', wvf_byc[0].shape)
        # print('wvf_byc[1].shape =', wvf_byc[1].shape)
        # print('times_byc[0].shape =', times_byc[0].shape)
        # print('times_byc[1].shape =', times_byc[1].shape)

        # n_samples = wvf_byc[0].shape[1]
        # wvf_1by1 = [[np.zeros((0, n_samples), dtype=np.double)]]
        # times_1by1 = [[np.zeros((0, 1), dtype=np.double)]]

        # print('before concatenation:')
        # print('wvf_1by1[0].shape =', wvf_1by1[0].shape)
        # print('times_1by1[0].shape =', times_1by1[0].shape)

        # wvf_1by1[0][0] = np.concatenate((wvf_1by1[0][0], wvf_byc[orig_electrodeID]), axis=0)
        # times_1by1[0][0] = np.concatenate((times_1by1[0][0], times_byc[orig_electrodeID]), axis=0)

        # print('after concatenation:')
        # print('wvf_1by1[0].shape =', wvf_1by1[0].shape)
        # print('times_1by1[0].shape =', times_1by1[0].shape)

        divided = dict(wvf_single_channel=wvf_byc[orig_electrodeID], times_single_channel=times_byc[orig_electrodeID])
        new_electrodeID = str(orig_electrodeID + 1)
        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID_without_s + '_single_channel.mat'
        trg_path = trg_dir + '/' + trg_fileName
        # print(src_path, '->', trg_path)
        scipy_savemat(trg_path, divided)
        # hdf5_savemat(trg_path, divided, format='7.3', oned_as='column')
