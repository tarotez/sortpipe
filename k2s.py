import numpy as np
from scipy.io import savemat as scipy_savemat
from hdf5storage import savemat as hdf5_savemat
from mainfunc.converter import convert
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

params = read_config()
primary_electrodeL_by_subsession = []
for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.for_stability_analysis_dir, '.mat'):
    print('subsession_path =', subsession_path)
    sessionID = subsession_path.split('/')[0]
    make_directories(params.for_stability_analysis_dir + '/' + subsession_path)
    in_path = params.kilo_sorted_dir + '/' + subsession_path
    out_path = params.for_stability_analysis_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    converted, primary_electrodeL = convert(in_path, np.double(params.sample_rate), int(params.n_electrodes), np.double(params.wvf_amplitude_scaling))    
    primary_electrodeL_by_subsession.append(primary_electrodeL)
    # print('the size of the wvf is', getsizeof(converted['wvf']))
    # if getsizeof(converted['wvf']) < 1000 * 1000 * 1000:
    #    print('saving in Matlab 5 format.')
    #    scipy_savemat(out_path, converted)
    # else:
    #    print('saving in Matlab 7.3 format.')        
    #    hdf5_savemat(out_path, converted, format='7.3', oned_as='column')
    print('out_path =', out_path)
    hdf5_savemat(out_path, converted, format='7.3', oned_as='column')
    # hdf5_savemat(out_path, times_units_electrodes, format='7.3', oned_as='column')

    # write out primary_electrodeL
    ###
    ### out_path = params.for_stability_analysis_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    primary_electrode_path = params.for_stability_analysis_dir + '/' + subsession_path + '/' + sessionID + '_unit2chan.csv'
    ###
    with open(primary_electrode_path, 'w') as fH:
        for unitID, electrodeID in  enumerate(primary_electrodeL):
            fH.write(str(unitID + 1) + ', ' + str(electrodeID + 1) + '\n')

for subsession_path in get_unprocessed(params.for_stability_analysis_dir, params.matrix_not_cell_array_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    subsessionID_without_s = subsessionID[1:]
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    ### trg_dir = params.matrix_not_cell_array_dir + '/' + sessionID + '/elc_01plx'
    trg_dir = params.matrix_not_cell_array_dir + '/' + sessionID + '/' + subsessionID + '/elc_01plx'
    make_directories(trg_dir)

    ### orig_dict = hdf5_loadmat(src_path)
    ### wvf_byc = orig_dict['wvf']
    ### times_byc = orig_dict['times']
    wvf_byc = converted['wvf']
    times_byc = converted['times']
    # print('times_byc =')
    # print(times_byc)
    # print('times_byc.shape =', times_byc.shape)
    print('len(wvf_byc) =', len(wvf_byc))

    for orig_electrodeID in range(len(wvf_byc)):
        
        print('wvf_byc[0].shape =', wvf_byc[0].shape)
        print('wvf_byc[1].shape =', wvf_byc[1].shape)
        print('times_byc[0].shape =', times_byc[0].shape)
        print('times_byc[1].shape =', times_byc[1].shape)

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
        print('divided =', divided)
        print(src_path, '->', trg_path)
        scipy_savemat(trg_path, divided)
        # hdf5_savemat(trg_path, divided, format='7.3', oned_as='column')
