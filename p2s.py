import shutil as sh
from os import listdir
from lib.manage_params import read_config
from lib.manage_files import get_unprocessed, make_directories

params = read_config()

for subsession_path in get_unprocessed(params.manually_sorted_dir, params.for_stability_analysis_dir, 'mat'):

    make_directories(params.for_stability_analysis_dir, subsession_path)
    src_dir = params.manually_sorted_dir + '/' + subsession_path
    trg_dir = params.for_stability_analysis_dir + '/' + subsession_path

    sessionID, subsessionID = subsession_path.split('/')    

    for src_file in listdir(src_dir):        
        src_path = src_dir + '/' + src_file        
        elems = src_file.split('.')[0].split('_')
        print(elems)
        if elems[1] == 'sort':
            orig_electrodeID = elems[2]
            new_electrodeID = str(int(orig_electrodeID) + 1)
            trg_file = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '_sort.mat'
            # print(src_file, '->', trg_file)
            trg_path = trg_dir + '/' + trg_file
            print(src_path, '->', trg_path)
            sh.copyfile(src_path, trg_path)
