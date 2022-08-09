
config_dict = read_config;

src_dir = config_dict('for_stability_analysis_dir');
sess_filenames = {dir(src_dir).name};

for i = 4:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    sess_dir = src_dir + "/" + sess_filename + "/elc_01plx";
    subsess_filenames = {dir(sess_dir).name};
    
    for j = 3:size(subsess_filenames,2)    
        subsess_filename = subsess_filenames{j};
        subsess_file_path = sess_dir + '/' + subsess_filename;
        load(subsess_file_path)
        wvf = cell(1);
        times = cell(1);
        wvf{1,1} = wvf_single_channel;
        times{1,1} = times_single_channel;
        save(subsess_file_path, 'wvf', 'times', 'wvf_single_channel', 'times_single_channel');        
        clear
    end
end