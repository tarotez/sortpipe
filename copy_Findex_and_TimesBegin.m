
config_dict = read_config;

src_dir = config_dict('behavior_dir');
target_dir = config_dict('for_stability_analysis_dir');
sess_filenames = {dir(src_dir).name};

for i = 4:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    src_sess_dir = src_dir + "/" + sess_filename + "/elc_01plx";
    target_sess_dir = target_dir + "/" + sess_filename + "/elc_01plx";    
    subsess_filenames = {dir(src_sess_dir).name};
    
    for j = 3:size(subsess_filenames,2)    
        subsess_filename = subsess_filenames{j};
        if endsWith(subsess_filename, ".mat")
            src_file_path = src_sess_dir + '/' + subsess_filename;
            fprintf("%s\n", src_file_path)                        
            target_file_path = target_sess_dir + '/' + target_subsess_filename;
            load(src_file_path)
            load(target_file_path)
            fprintf("  -> %s\n", target_file_path)
            save(target_file_path, 'wvf', 'times', 'Findex', 'TimesBegin');
        end
        
    end
end