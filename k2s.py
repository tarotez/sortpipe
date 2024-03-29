import shutil as sh
import numpy as np
# from os import listdir
from os.path import exists
from scipy.io import savemat as scipy_savemat
from hdf5storage import savemat as hdf5_savemat
from hdf5storage import loadmat as hdf5_loadmat
from mainfunc.converter import convert
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, get_all_paths, get_all_sessionIDs, make_directories

params = read_config()

# convert phy file into matlab format
primary_electrodeL_by_subsession = []
in_dir_for_conversion = params.kilo_sorted_dir
out_dir_for_conversion = params.plexon_input_dir
for subsession_path in get_unprocessed(in_dir_for_conversion, out_dir_for_conversion, '.mat'):
    print('kilo_sorted -> plexon_input_dir, subsession_path =', subsession_path)
    sessionID = subsession_path.split('/')[0]
    make_directories(out_dir_for_conversion + '/' + subsession_path)
    in_path = in_dir_for_conversion + '/' + subsession_path
    out_path = out_dir_for_conversion + '/' + subsession_path + '/' + sessionID + '.mat'
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
    ### out_path = params.for_stability_analysis_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    primary_electrode_dir = params.for_stability_analysis_dir + '/' + subsession_path
    primary_electrode_path = primary_electrode_dir + '/' + sessionID + '_unit2chan.csv'
    make_directories(primary_electrode_dir)
    with open(primary_electrode_path, 'w') as fH:
        for unitID, electrodeID in  enumerate(primary_electrodeL):
            fH.write(str(unitID + 1) + ', ' + str(electrodeID + 1) + '\n')

# divide into chennels (one file for one channel, i.e. electrode) and write out _single_channel_sort.mat files.
in_dir_for_division = params.plexon_input_dir
out_dir_for_division = params.matrix_not_cell_array_dir
# for subsession_path in get_unprocessed(in_dir_for_division, out_dir_for_division, '.mat'):
for subsession_path in get_all_paths(in_dir_for_division):
    print('stability -> matrix_not_cell_array, subsession_path =', subsession_path)
    sessionID = subsession_path.split('/')[0]
    in_path = in_dir_for_division + '/' + subsession_path + '/' + sessionID + '.mat'
    converted = hdf5_loadmat(in_path, format='7.3', oned_as='column')

    # print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    subsessionID_without_s = subsessionID[1:]
    src_path = in_dir_for_division + '/' + subsession_path + '/' + sessionID + '.mat'
    ### trg_dir = out_dir_for_division + '/' + sessionID + '/elc_01plx'
    trg_dir = out_dir_for_division + '/' + sessionID + '/' + subsessionID + '/elc_01plx'
    make_directories(trg_dir)

    ### orig_dict = hdf5_loadmat(src_path)
    ### wvf_byc = orig_dict['wvf']
    ### times_byc = orig_dict['times']
    wvf_byc = converted['wvf']
    times_byc = converted['times']
    # print('times_byc =')
    # print(times_byc)
    # print('times_byc.shape =', times_byc.shape)
    # print('len(wvf_byc) =', len(wvf_byc))
    for orig_electrodeID in range(len(wvf_byc)):        
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
        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID_without_s + '_single_channel_sort.mat'
        trg_path = trg_dir + '/' + trg_fileName
        # print('divided =', divided)
        print(src_path, '->', trg_path)
        scipy_savemat(trg_path, divided)
        # hdf5_savemat(trg_path, divided, format='7.3', oned_as='column')

# copy behavior files
src_root = params.behavior_dir
trg_root = params.for_stability_analysis_dir
edf_dirName = 'EDfiles'
info_dirName = 'Info'

# for subsession_path in get_existing(src_root, trg_root):
for subsession_path in get_all_sessionIDs(src_root):

    # print('subsession_path =', subsession_path)
    sessionID = subsession_path.split('/')[-1]
    # print('sessionID = ', sessionID)
    
    src_dir = src_root + '/' + sessionID + '/'
    # trg_dir = params.for_stability_analysis_dir + '/' + sessionID + '/'
    trg_dir = trg_root + '/' + sessionID + '/'
    # make_directories(trg_dir)

    edf_src = src_dir + edf_dirName
    edf_trg = trg_dir + edf_dirName
    info_src = src_dir + info_dirName
    info_trg = trg_dir + info_dirName

    if not exists(edf_trg):
        sh.copytree(edf_src, edf_trg)
    if not exists(info_trg):
        sh.copytree(info_src, info_trg)
