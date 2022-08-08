import numpy as np
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

    orig_data = hdf5_loadmat(src_path)
    wvf_byc = orig_data['wvf']
    times_byc = orig_data['times']
    # print('times.shape =', times.shape)

    for orig_electrodeID in range(len(wvf_byc)):
        # print('times.shape =', times[orig_electrodeID].shape)

        # wvf_byc = [np.zeros((0, n_samples)) for _ in range(n_channels)]         
        # wvf_1by1 = np.array([np.array([wvf[orig_electrodeID]], dtype=np.double)], dtype=object)
        # times_1by1 = np.array([np.array([times[orig_electrodeID]], dtype=np.double)], dtype=object)
        
        print('wvf_byc[0].shape =', wvf_byc[0].shape)
        print('wvf_byc[1].shape =', wvf_byc[1].shape)
        print('times_byc[0].shape =', times_byc[0].shape)
        print('times_byc[1].shape =', times_byc[1].shape)

        n_samples = wvf_byc[0].shape[1]
        wvf_1by1 = [np.zeros((0, n_samples))]
        times_1by1 = [np.zeros((0), dtype=np.double)]

        print('before concatenation:')
        print('wvf_1by1[0].shape =', wvf_1by1[0].shape)
        print('times_1by1[0].shape =', times_1by1[0].shape)

        # np.concatenate((wvf_byc[prim_elec], waveforms), axis=0)
        wvf_1by1[0] = np.concatenate((wvf_1by1[0], wvf_byc[orig_electrodeID]), axis=0)
        # times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID]), axis=0)
        # times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID].transpose()), axis=0)
        times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID][np.newaxis].transpose()), axis=0)
        ### also try:
        # times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID]))
        ### times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID][np.newaxis].transpose()), axis=0)
        ### times_1by1[0] = np.concatenate((times_1by1[0], times_byc[orig_electrodeID][np.newaxis]), axis=0)

        print('after concatenation:')
        print('wvf_1by1[0].shape =', wvf_1by1[0].shape)
        print('times_1by1[0].shape =', times_1by1[0].shape)

        divided = dict(wvf=np.array(wvf_1by1, dtype=object), times=np.array(times_1by1, dtype=object))
        new_electrodeID = str(orig_electrodeID + 1)
        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '.mat'
        trg_path = trg_dir + '/' + trg_fileName
        hdf5_savemat(trg_path, divided, format='7.3', oned_as='column')
        