function config_dict = read_config()
    fID = fopen('config/sortpipe_config.csv');
    config_dict = containers.Map;
    while ~feof(fID)
       line = fgetl(fID);
       split = regexp(line, ', ', 'split');
       key = split{1};
       value = split{2};
       config_dict(key) = value;
    end
