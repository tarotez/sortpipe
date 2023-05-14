config_dict = read_config;
src_dir = config_dict('behavior_dir');
target_dir = config_dict('for_stability_analysis_dir');
sess_names = {dir(src_dir).name};
for i = 1:size(sess_names,2)
    sess_name = sess_names{i};
    if startsWith(sess_name, ".")
        continue
    end
    src_file_path = src_dir + "/" + sess_name + "/Info/" + sess_name + "_param.mat";
    if isfile(src_file_path)                                       
        fprintf("%s\n", src_file_path)
        load(src_file_path)
        % loop over all subsessions
        target_sess_dir = target_dir + "/" + sess_name;
        target_sess_dir_struct = dir(target_sess_dir);
        subsess_names = {target_sess_dir_struct.name};           
        for j = 1:size(subsess_names,2)
            subsess_name = subsess_names{j};
            if startsWith(subsess_name, ".") || strcmp(subsess_name, "Info") || strcmp(subsess_name, "EDfiles") || strcmp(subsess_name, "plxMergeEDfiles")
                continue
            end
            target_subsess_dir = target_dir + "/" + sess_name + "/" + subsess_name + "/elc_01plx";
            target_subsess_dir_struct = dir(target_subsess_dir);
            recording_filenames = {target_subsess_dir_struct.name};
            for k = 1:size(recording_filenames,2)            
                recording_filename = recording_filenames{k};
                if endsWith(recording_filename, ".mat")
                    target_file_path = target_subsess_dir + "/" + recording_filename;                                                        
                    fprintf("  -> %s\n", target_file_path)
                    save(target_file_path, 'wvf', 'times', 'Findex', 'TimesBegin');                
                end
            end
        end
    end
end