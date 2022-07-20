from os import listdir, mkdir
from os.path import exists, splitext

def get_all_paths(root_dir):
    paths = []
    for session in listdir(root_dir):
        if not session.startswith('.'):
            for subsession in listdir(root_dir + '/' + session):
                if not subsession.startswith('.'):
                    paths.append(session + '/' + subsession)
    return paths

def filter_out_processed(input_paths, out_dir, target_suffix):
    unprocessed_paths = []
    for input_path in input_paths:
        if exists(out_dir + '/' + input_path):
            flag = 1
            for filename in listdir(out_dir + '/' + input_path):
                if filename.endswith(target_suffix):
                    flag = 0
            if flag:
                unprocessed_paths.append(input_path)                
        else:
            unprocessed_paths.append(input_path)
    return unprocessed_paths

def get_unprocessed(in_dir, out_dir, target_suffix):
    return filter_out_processed(get_all_paths(in_dir), out_dir, target_suffix)

def make_directories(path):
    elems = path.split('/')
    path_super = elems[0]
    for dir_str in elems[1:]:
        # print('dir_str =', dir_str)
        path_super += '/' + dir_str
        # print('checking if', path_super, 'exists.')            
        if not exists(path_super):
            # print('making', path_super, 'directory.')
            mkdir(path_super)

