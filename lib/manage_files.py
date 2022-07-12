from os import listdir, mkdir
from os.path import exists

def get_all_paths(root_dir, sep):
    paths = []
    for session in listdir(root_dir):
        if not session.startswith('.'):
            for subsession in listdir(root_dir + sep + session):
                if not subsession.startswith('.'):
                    paths.append(session + sep + subsession)
    return paths

def filter_out_processed(input_paths, out_dir, output_mat_file_name, sep):
    unprocessed_paths = []
    for input_path in input_paths:        
        if not exists(out_dir + sep + input_path + sep + output_mat_file_name):
            unprocessed_paths.append(input_path)
    return unprocessed_paths

def get_unprocessed(in_dir, out_dir, output_mat_file_name, sep):
    return filter_out_processed(get_all_paths(in_dir, sep), out_dir, output_mat_file_name, sep)

def make_directories(root_dir, path, sep):
    elems = path.split(sep)
    path_super = root_dir + sep
    for dir_str in elems:
        path_super += dir_str + sep
        # print('checking if', path_super, 'exists.')            
        if not exists(path_super):
            # print('making', path_super, 'directory.')
            mkdir(path_super)

