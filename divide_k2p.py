import hdf5storage
from lib.manage_files import get_unprocessed, make_directories
from lib.manage_params import read_config

params = read_config()

for subsession_path in get_unprocessed(params.plexon_input_dir, params.for_stability_analysis_dir, 'mat'):

    print('subsession_path =', subsession_path)
    make_directories(params.for_stability_analysis_dir, subsession_path)
    
    in_path = params.plexon_input_dir + '/' + subsession_path + '/' + params.output_mat_file_name
    out_dir = params.for_stability_analysis_dir + '/' + subsession_path

    # orig_data = hdf5storage.loadmat(orig_path, format='7.3', oned_as='column')
    orig_data = hdf5storage.loadmat(in_path)
    wvf = orig_data['wvf']
    times = orig_data['times']

    for orig_electrodeID in range(len(wvf)):

        wvf_elem = wvf[orig_electrodeID]
        times_elem = times[orig_electrodeID]
        divided = dict(wvf=wvf_elem, times=times_elem)
        new_electrodeID = orig_electrodeID + 1
        sessionID = ...
        subsessionID = ...



        trg_fileName = sessionID + '_el' + new_electrodeID + '_subsess' + subsessionID + '.mat'
        out_path = out_dir + '/' + trg_fileName
        hdf5storage.savemat(out_path, divided, format='7.3', oned_as='column')
