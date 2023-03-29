# SortPipe: automatic pipeline from kilosort to plexon offline sorter

## Directory structure:

Requires to put a config file (sortpipe_config.csv) in a directory named "config".

sortpipe (this repository)\
-- mainfunc\
-- lib\
config\
-- sortpipe_config.csv

## Example config file (sortpipe_config.csv):

MNAME is the monkey identifier, such as Nana32.

sample_rate, 30000\
n_electrodes, 32\
kilo_sorted_dir, ../../data/kiloSorted_MNAME\
plexon_input_dir, ../../data/toPlexonOfflineSorter_MNAME\
manually_sorted_dir, ../../data/toPlexonOfflineSorter_MNAME\
for_stability_analysis_dir, ../../data/forStabilityAnalysis_MNAME

### Data processing pipeline

1.  Run MATLAB/bin_file_generator/createData4Kilo.m to convert recordings to the bin format. The result will be in D:\\rawData_MNAME, where MNAME is the identifier for the monkey.

2. Run Documents/autokilo to apply kilosort to all files. The result will be in D:\\kiloSorted_MNAME. Some of the files are in the Phy format.

3. Click kilo2plexon.bat on the desktop to write out D:\\toPlexonOfflineSorter/sessionXX/subsessionZ/sessionXX.mat. It contains waveforms and spike times converted from files in D:\\kiloSorted_MNAME in the Phy format.

4. Start Plexon Offline Sorter. Go to File -> Import -> Spike Data from MATLAB and open toPlexonOfflineSorter/sessionXX/subsessionZ/sessionXX.mat files, and do manual sorting.

5. Go to File -> Export Per-waveform Data. Select "Matlab file" as Format.

    a. Choose All Channels, All Units, One file per channel.

    b. Check "Import unit designation", select a designation. Usually, there's only one choice.

    c. Removing check marks from PC1 and PC2 can save some disk space.

    d. Can write out to toPlexonOfflineSorter/sessionXX/subsessionZ/sessionXX.mat, which is the same directory as the input directory.

    e. The output files are "sessionXX_YYY.mat" where "_YYY" indicate channel numbers. Each of this file contains wvf0 (matrix).

    f. Sometimes, an error message shows up saying "the file is already opened by Microsoft Excel". In that case, make a new directory and write out there.

6. Click plexon2stability.bat on the Desktop. It transorms toPlexonOfflineSorter/sessionXX/subsessionZ/sessionXX_YYY.mat into sessionXX_elYY_subsessZ_single_channel_sort.mat and copies to matrixNotCellArray_MNAME/sessionXX.

7. Click divide_by_channel.bat on the Desktop. It generates matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat for each single unit (channel). The mat files contain variables wvf_single_channel and times_single_channel.

8. From Matlab, execute Documents/kilo2plexon/sortpipe/convert_to_1x1_cell_array.m to convert wvf_single_channel (matrix)
 in matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat to wvf (1x1 cell array), and times_single_channel to times (1x1 cell array), then save them in sessionXX_elYY_subsessZ.mat. Also convert wvfY (matrix) in forStabilityAnalysis_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel_sort.mat to wvf (1x1 cell array).

9. Click copy_behavior.bat on the Desktop. It copies behavioral data (EDfiles and Info) in Z:\\prut.lab\\Nana_DAQ to forStabilityAnalysis_MNAME//sessionXX. It generates three directories elc_01plx, EDfiles, Info in D:\\forStabilityAnalysis_MNAME/sessionXX.

10. From Matlab, execute D:\\Nana_programs_updated\\sortUtils\\MergePlx2EDs to merge spike trains and behavioral data to generate files in the directory, plxMergeEDfiles.

11. Carry out stability analysis using the following command:

cd D:\\Nana_programs_updated\\sortUtils
MergePlx2EDs('D:\\forStabilityAnalysis_MNAME\\', 'n300122');

(The final "\\" of the first argument is required).

It generates D:\\forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles.

12. From Matlab, execute the stability analysis program, and read D:\\forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles from the GUI.
