config_dict = read_config;

% src_dir = config_dict('for_stability_analysis_dir');
% sess_filenames = {dir(src_dir).name};

for i = 4:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    sess_dir = src_dir + "/" + sess_filename + "/elc_01plx";
    subsess_filenames = {dir(sess_dir).name};

    src = 
    dst = 

    os.symlink(src, dst)
    
end