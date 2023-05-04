config_dict = read_config;

src_dir = config_dict('matrix_not_cell_array_dir');
target_dir = config_dict('for_stability_analysis_dir');
%%% sess_filenames = {dir(src_dir).name};
src_dir_struct = dir(src_dir);
sess_filenames = {src_dir_struct.name};
for i = 1:size(sess_filenames,2)
    sess_filename = sess_filenames{i};
    if startsWith(sess_filename, ".")
        continue
    end
    src_sess_dir = src_dir + "/" + sess_filename;
    target_sess_dir = target_dir + "/" + sess_filename;        
    %%% subsess_filenames = {dir(src_sess_dir).name};
    src_sess_dir_struct = dir(src_sess_dir);
    subsess_filenames = {src_sess_dir_struct.name};
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
            if startsWith(recording_filename, ".")
                continue
            end            
            %%% if endsWith(recording_filename, "_single_channel.mat")
            if endsWith(recording_filename, "_single_channel_sort.mat")
                src_file_path = src_sess_dir + "/" + subsess_filename + "/elc_01plx/" + recording_filename;
                % fprintf("%s\n", src_file_path)            
                load(src_file_path)
                wvf = cell(1);
                times = cell(1);
                wvf{1,1} = wvf_single_channel;
                times{1,1} = times_single_channel;
                target_recording_filename = strrep(recording_filename, "_single_channel", "");
                target_file_path = target_sess_dir + "/" + subsess_filename + "/elc_01plx/" + target_recording_filename;
                if ~isdir(target_sess_dir + "/" + subsess_filename + "/elc_01plx/")
                    mkdir(target_sess_dir + "/" + subsess_filename + "/elc_01plx/")
                end
                if ~isfile(target_file_path)
                    fprintf("  -> %s\n", target_file_path)
                    save(target_file_path, 'wvf', 'times');            
                % else
                %    fprintf("  -> target file %s already exists.\n", target_file_path)
                end
            end
            % if endsWith(recording_filename, "_single_channel_sort.mat")
            %     src_file_path = src_sess_dir + '/' + subsess_filename + "/elc_01plx/" + recording_filename;
            %     fprintf("%s\n", src_file_path)  
            %     load(src_file_path)                 
            %     elems = split(recording_filename, '_');
            %     channelID_one_origin = strrep(elems(2), "el", '');
            %     channelID_zero_origin = int2str(str2num(channelID_one_origin{1}) - 1);
            %     eval("wvf0 = wvf" + channelID_zero_origin + ";");
            %     target_recording_filename = strrep(recordig_filename, "_single_channel", "");
            %     target_file_path = target_sess_dir + "/" + subsess_filename + "/" + target_recording_filename;
            %     if ~isfile(target_file_path)
            %         fprintf("  -> %s\n", target_file_path)
            %         save(target_file_path, 'wvf0');
            %     else
            %         fprintf("  -> target file %s already exists.\n", target_file_path)
            %     end
            % end
        end
    end
end