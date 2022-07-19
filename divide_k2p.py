import hdf5storage
# from lib.manage_files import get_unprocessed, make_directories



# for subsession_path in get_unprocessed(params.kilo_sorted_dir, params.plexon_input_dir, params.output_mat_file_name, sep):

for subsession_path in ...:

    print('subsession_path =', subsession_path)

    # make_directories(params.plexon_input_dir, subsession_path, sep)

    in_path = params.kilo_sorted_dir + '/' + subsession_path
    
    out_path = params.plexon_input_dir + '/' + subsession_path + '/' + output_mat_file_name
    

    orig_path = '...'

    # orig_data = hdf5storage.loadmat(orig_path, format='7.3', oned_as='column')
    orig_data = hdf5storage.loadmat(orig_path, oned_as='column')

    dividedL = []
    for ... in ...:

        dividedL.append()

    divided = ...


    hdf5storage.savemat(out_path, divided, format='7.3', oned_as='column')