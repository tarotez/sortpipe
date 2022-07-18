import shutil as sh
from os import listdir
# from lib.manage_params import read_config

# params = read_config()
# sep = params.sep

# params.plexon_input_dir + sep + subsession_path
### src_root_dir = 'D:/manuallyRefined_Nana32'
src_root_dir = '../../manuallyRefined_Nana32'
trg_root_dir = '../../forStabilityAnalysis_Nana32'
sessionID = 'n010222'
subsessionID = '1'
src_dir = src_root_dir + '/' + sessionID + '/s' + subsessionID
trg_dir = trg_root_dir + '/' + sessionID + '/s' + subsessionID

# for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.plexon_input_dir, params.output_mat_file_name, sep):
for src_file in listdir(src_dir):
    src_path = src_dir + '/' + src_file
    elems = src_file.split('.')[0].split('_')
    if elems[1] == 'sort':
        orig_electrodeID = elems[2]
        new_electrodeID = str(int(orig_electrodeID) + 1)
        trg_file = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '_sort.mat'
        # print(src_file, '->', trg_file)
        trg_path = trg_dir + '/' + trg_file
        print(src_path, '->', trg_path)
        sh.copyfile(src_path, trg_path)
