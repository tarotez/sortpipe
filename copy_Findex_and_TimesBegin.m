
config_dict = read_config;

src_dir = config_dict('behavior_dir');
target_dir = config_dict('for_stability_analysis_dir');
sess_filenames = {dir(src_dir).name};

% for i = 4:size(sess_filenames,2)
for i = 1:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    if startsWith(sess_filename, ".")
        continue
    end
    src_sess_dir = src_dir + "/" + sess_filename;
    target_sess_dir = target_dir + "/" + sess_filename;
    src_sess_dir_struct = dir(src_sess_dir);
    subsess_filenames = {src_sess_dir_struct.name};    
    % subsess_filenames = {dir(src_sess_dir).name};   
    % for j = 3:size(subsess_filenames,2)    
    %    subsess_filename = subsess_filenames{j};    
    for j = 1:size(subsess_filenames,2)
        subsess_filename = subsess_filenames{j};
        if startsWith(subsess_filename, ".")
            continue
        end
        src_subsess_dir = src_dir + "/" + sess_filename + "/" + subsess_filename + "/elc_01plx";
        src_subsess_dir_struct = dir(src_subsess_dir);
        recording_filenames = {src_subsess_dir_struct.name};
        for k = 1:size(recording_filenames,2)            
            recording_filename = recording_filenames{k};
            if endsWith(recording_filename, ".mat")
                src_file_path = src_sess_dir + "/" + subsess_filename + + "/elc_01plx/" + recording_filename;
                target_file_path = target_sess_dir + "/" + subsess_filename + "/elc_01plx/" + recording_filename;
                if isfile(src_file_path) && isfile(target_file_path)
                    load(src_file_path)
                    load(target_file_path)
                    fprintf("%s\n", src_file_path)              
                    fprintf("  -> %s\n", target_file_path)
                    save(target_file_path, 'wvf', 'times', 'Findex', 'TimesBegin');
                end
            end        
        end
    end
end