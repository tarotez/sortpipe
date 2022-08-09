from os import symlink
from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

for subsession_path in get_unprocessed(params.plexon_input_dir, params.for_stability_analysis_dir, '.mat'):

    print('subsession_path =', subsession_path)
    sessionID, subsessionID = subsession_path.split('/')
    src_path = params.plexon_input_dir + '/' + subsession_path + '/' + sessionID + '.mat'
    trg_dir = params.for_stability_analysis_dir + '/' + sessionID 
    make_directories(trg_dir)

    edf_src = src_dir +
    edf_trg = trg_dir +
    inf_src = src_dir + 
    inf_trg = trg_dir + 

    symlink(edf_src, edf_trg)
    symlink(inf_src, inf_trg)

    
