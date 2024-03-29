import shutil as sh
from os.path import exists
from lib.manage_files import get_existing
# from lib.manage_files make_directories
from lib.manage_params import read_config

params = read_config()

src_root = params.behavior_dir
trg_root = params.for_stability_analysis_dir
edf_dirName = 'EDfiles'
info_dirName = 'Info'

for subsession_path in get_existing(src_root, trg_root):

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

    # print('edf_src =', edf_src)
    # print('edf_trg =', edf_trg)

    if not exists(edf_trg):
        sh.copytree(edf_src, edf_trg)
    if not exists(info_trg):
        sh.copytree(info_src, info_trg)

    
