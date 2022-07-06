from bunch import Bunch
import pandas as pd

def read_config():

    config_path = '../'
    # settings = pd.read_csv(config_path, sep='\t')

    params = Bunch()
    params.sample_rate = 30000   # sampling rate used by the electrodes
    params.n_electrodes = 32   # number of electrodes
    params.kilo_sorted_dir = '../../kiloSorted_Nana32'
    params.plexon_input_dir = '../../plexonSorterInput_Nana32'

    return params

