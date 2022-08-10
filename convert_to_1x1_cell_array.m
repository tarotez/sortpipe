
config_dict = read_config;

src_dir = config_dict('for_stability_analysis_dir');
sess_filenames = {dir(src_dir).name};

for i = 4:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    sess_dir = src_dir + "/" + sess_filename + "/elc_01plx";
    subsess_filenames = {dir(sess_dir).name};
    
    for j = 3:size(subsess_filenames,2)    
        subsess_filename = subsess_filenames{j};
        if endsWith(subsess_filename, "_single_channel.mat")
            in_file_path = sess_dir + '/' + subsess_filename;
            load(in_file_path)
            wvf = cell(1);
            times = cell(1);
            wvf{1,1} = wvf_single_channel;
            times{1,1} = times_single_channel;
            out_file_path = strrep(in_file_path, "_single_channel", "");
            save(out_file_path, 'wvf', 'times');
        end
        
        if endsWith(subsess_filename, "_single_channel_sort.mat")
            in_file_path = sess_dir + '/' + subsess_filename;
            load(in_file_path)
            wvf0 = cell(1);
                        
            channelID_zero_origin = get_channelID(subsess_filename);
            
            
            eval('wvf0{1,1} = wvf' + channelID_zero_origin);
            out_file_path = strrep(in_file_path, "_single_channel", "");
            save(out_file_path, 'wvf0');
        end
        
    end
end