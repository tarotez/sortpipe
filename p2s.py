import shutil as sh
from os import listdir
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

params = read_config()

for subsession_path in get_unprocessed(params.manually_sorted_dir, params.matrix_not_cell_array_dir, '.mat'):

    print('subsession_path =', subsession_path)
    src_dir = params.manually_sorted_dir + '/' + subsession_path
    sessionID, subsessionID = subsession_path.split('/')
    subsessionID_without_s = subsessionID[1:]
    trg_dir = params.matrix_not_cell_array_dir + '/' + sessionID + '/elc_01plx'
    make_directories(trg_dir)

    for src_file in listdir(src_dir):        
        src_path = src_dir + '/' + src_file        
        elems = src_file.split('.')[0].split('_')
        # print(elems)
        if len(elems) > 3:
            print('File name has too many underscores in', src_file)
            print('It should be SESSIONID_ELECTRODEID.mat or SESSIONID_SUFFIX_ELECTRODEID.mat.')
        if len(elems) == 2 or len(elems) == 3:
            orig_electrodeID = elems[-1]
            new_electrodeID = str(int(orig_electrodeID) + 1)
            trg_file = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID_without_s + '_single_channel_sort.mat'
            # print(src_file, '->', trg_file)
            trg_path = trg_dir + '/' + trg_file
            print(src_path, '->', trg_path)
            # sh.move(src_path, trg_path)
            sh.copyfile(src_path, trg_path)
