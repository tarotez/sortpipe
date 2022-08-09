from os import symlink
from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

edf_suffix = ''
info_suffix = ''

for subsession_path in get_unprocessed(params.plexon_input_dir, params.for_stability_analysis_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    
    src_dir = 

    

    trg_dir = params.for_stability_analysis_dir + '/' + sessionID 
    make_directories(trg_dir)

    edf_src = src_dir + edf_suffix
    edf_trg = trg_dir + edf_suffix
    info_src = src_dir + info_suffix
    info_trg = trg_dir + info_suffix

    symlink(edf_src, edf_trg)
    symlink(info_src, info_trg)

    
