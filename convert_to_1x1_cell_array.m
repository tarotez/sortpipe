
src_dir = "../../data/forStabilityAnalysis_Nana32";
filenames = {dir(src_dir).names};

for i = size(filenames,2)

    filename = filenames(i);
    
    src_filename = '';

    in_dir = [src_dir src_filename];
    load(in_dir)

    one_by_one_cell_array = 

    save(out_dir, one_by_one_cell_array);

end