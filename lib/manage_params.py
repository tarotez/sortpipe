from bunch import Bunch

def read_config():

    params = Bunch()
    params.sep = "/"
    with open('../../config/sortpipe_config.csv') as f:
        for line in f:
            key, val = line.rstrip().split(',')
            params[key.rstrip()] = val.lstrip()

    return params