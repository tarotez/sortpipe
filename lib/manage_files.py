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

def filter_out_processed(input_paths, out_dir, target_extension):
    unprocessed_paths = []
    for input_path in input_paths:
        for filename in listdir(out_dir + '/' + input_path):
            ext = splitext(filename)[1]
            if ext.endswith(target_extension):
                unprocessed_paths.append(input_path)
                break
    return unprocessed_paths

def get_unprocessed(in_dir, out_dir, target_extension):
    return filter_out_processed(get_all_paths(in_dir), out_dir, target_extension)

def make_directories(root_dir, path):
    elems = path.split('/')
    path_super = root_dir + '/'
    for dir_str in elems:
        path_super += dir_str + '/'
        # print('checking if', path_super, 'exists.')            
        if not exists(path_super):
            # print('making', path_super, 'directory.')
            mkdir(path_super)

