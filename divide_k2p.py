import hdf5storage
from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()
sep = params.sep

for subsession_path in get_unprocessed(params.plexon_sorted_dir, params.for_stability_analysis_dir, params.output_mat_file_name, sep):

    print('subsession_path =', subsession_path)
    # make_directories(params.plexon_input_dir, subsession_path, sep)
    
    in_path = params.plexon_input_dir + '/' + subsession_path + '/' + params.output_mat_file_name
    out_dir = params.for_stability_analysis_dir + '/' + subsession_path

    # orig_data = hdf5storage.loadmat(orig_path, format='7.3', oned_as='column')
    orig_data = hdf5storage.loadmat(in_path, oned_as='column')
    wvf = orig_data.wvf
    times = orig_data.time3s

    for electrodeID in enumerate(len(wvf)):

        wvf_elem = wvf[electrodeID]
        times_elem = times[electrodeID]
        divided = dict(wvf=wvf_elem, times=times_elem)
        hdf5storage.savemat(out_dir, divided, format='7.3', oned_as='column')
