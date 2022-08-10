
config_dict = read_config;

src_dir = config_dict('matrix_not_cell_array_dir');
trg_dir = config_dict('for_stability_analysis_dir');
sess_filenames = {dir(src_dir).name};

for i = 4:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    src_sess_dir = src_dir + "/" + sess_filename + "/elc_01plx";
    trg_sess_dir = trg_dir + "/" + sess_filename + "/elc_01plx";
    
    %%% must make a directory for trg_sess_dir here?
    
    
    subsess_filenames = {dir(src_sess_dir).name};
    
    for j = 3:size(subsess_filenames,2)    
        subsess_filename = subsess_filenames{j};
        if endsWith(subsess_filename, "_single_channel.mat")
            src_file_path = src_sess_dir + '/' + subsess_filename;
            fprintf("%s\n", src_file_path)            
            load(src_file_path)
            wvf = cell(1);
            times = cell(1);
            wvf{1,1} = wvf_single_channel;
            times{1,1} = times_single_channel;
            trg_subsess_filename = strrep(subsess_filename, "_single_channel", "");
            trg_file_path = trg_sess_dir + '/' + trg_subsess_filename;
            if ~isfile(trg_file_path)
                fprintf("  -> %s\n", trg_file_path)
                save(trg_file_path, 'wvf', 'times');            
            else
                fprintf("  -> target file %s already exists.\n", trg_file_path)
            end
        end
        
        if endsWith(subsess_filename, "_single_channel_sort.mat")
            src_file_path = src_sess_dir + '/' + subsess_filename;                        
            fprintf("%s\n", src_file_path)  
            load(src_file_path)                                   
            elems = split(subsess_filename, '_');
            channelID_zero_origin = strrep(elems(2), 'el', '');
            eval('wvf0 = wvf' + channelID_zero_origin{1} + ';');
            trg_subsess_filename = strrep(subsess_filename, "_single_channel", "");
            trg_file_path = trg_sess_dir + '/' + trg_subsess_filename;            
            if isfile(grg_file_path)
                fprintf("  -> %s\n", trg_file_path)
                save(trg_file_path, 'wvf0');
            else
                fprintf("  -> target file %s already exists.\n", trg_file_path)
            end
        end
        
    end
end