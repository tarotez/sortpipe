from os import listdir, mkdir
from os.path import exists, splitext

def get_all_paths(root_dir):
    paths = []
    for session in listdir(root_dir):
        for subsession in listdir(root_dir + '/' + session):
            paths.append(session + '/' + subsession)
    return paths

def filter_out_processed(in_paths, already_processed_paths):
    unprocessed_paths = []
    for path in in_paths:
        if path not in already_processed_paths:
            unprocessed_paths.append(in_path)
    return unprocessed_paths

def get_unprocessed(in_dir, out_dir):
    return filter_out_processed(get_all_paths(in_dir), get_all_paths(out_dir))

def make_directories(paths):
    for path in paths:
        elems = path.split('/')
        path_super = ''
        for dir_str in elems[:-1]:
            path_super += dir_str + '/'
            if not exists(path_super):
                mkdir(path_super)

