# SortPipe: automatic pipeline from kilosort to plexon offline sorter

## Example config/sortpipe_config.csv file, specifying relevant directories.

```
sample_rate, 30000
n_electrodes, 32
wvf_amplitude_scaling, 0.2
kilo_sorted_dir, ../../data/kiloSorted_MNAME
plexon_input_dir, ../../data/toPlexonOfflineSorter_MNAME
manually_sorted_dir, ../../data/toPlexonOfflineSorter_MNAME
matrix_not_cell_array_dir, ../../data/matrixNotCellArray_MNAME
for_stability_analysis_dir, ../../data/forStabilityAnalysis_MNAME
behavior_dir, ../../data/MNAME_DAQ
```

### Data processing pipeline without manual sorting

Examples of batch (.bat) files that are referred to in this pipeline are in the directory "batch_examples". They may need to be edited so that the paths match that of the installed environment.

1. Run MATLAB/bin_file_generator/createData4Kilo.m to convert recordings to the bin format. The result will be in rawData_MNAME where MNAME is the identifier for the monkey.

2. Either run Kilosort GUI from Matlab, or run Documents/autokilo to apply kilosort to all files in rawData_MNAME. The result should be in the directory, kiloSorted_MNAME. Some of the files are in the Phy format, which cannot be read directly from Matlab. Hence the following steps are necessary for conversion. If running kilosort from GUI, set both the working directory and the final output directory to kiloSorted_MNAME, such that both "rez.mat" and "temp_wh.dat" files are written out to the same directory. 

3. Click kilo2stability.bat. It generates matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat for each single unit (channel). The mat files contain variables wvf_single_channel and times_single_channel. The program called by  kilo2stability.bat is k2s.py.

4. From Matlab, execute sortpipe/convert_to_1x1_cell_array.m. It does the following conversions to variables in matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat and write out to forStabilityAnalysis_MNAME.

    a. wvf_single_channel (matrix) ->  wvf (1x1 cell array)

    b. times_single_channel -> times (1x1 cell array), then save them in sessionXX_elYY_subsessZ.mat. Also convert wvfY (matrix) in forStabilityAnalysis/sessionXX/sessionXX_elYY_subsessZ_single_channel_sort.mat to wvf (1x1 cell array).

5. Click copy_behavior.bat. It copies behavioral data (EDfiles and Info) in behavior_dir (for example Z:\\prut.lab\\MNAME_DAQ or ../../data/MNAME) to forStabilityAnalysis//sessionXX. It also generates three directories elc_01plx, EDfiles, and Info in D:\\forStabilityAnalysis/sessionXX.

6. From Matlab, execute sortUtils\\MergePlx2EDs to merge spike trains and behavioral data. The output will be in the directory, plxMergeEDfiles.

7. Merge data by executing the following commands on a command line interface. The lines generate forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles. The final "\\" in the first argument is required.

```
cd D:\\KILOSORT\\sortUtils
MergePlx2EDs('D:\\KILOSORT\\data\\forStabilityAnalysis_MNAME\\', 'n220223\\s1');
```

8. From Matlab, execute the stability analysis program GUI, read forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles, and do stability analysis.


### Data processing pipeline with manual sorting by Plexon Offline Sorter

Examples of batch (.bat) files that are referred to in this pipeline are in the directory "batch_examples". They may need to be edited so that the paths match that of the installed environment.

1. Run MATLAB/bin_file_generator/createData4Kilo.m to convert recordings to the bin format. The result will be in rawData_MNAME where MNAME is the identifier for the monkey.

2. Either run Kilosort GUI from Matlab, or run Documents/autokilo to apply kilosort to all files in rawData_MNAME. The result should be in the directory, kiloSorted_MNAME. Some of the files are in the Phy format, which cannot be read directly from Matlab. Hence the following steps are necessary for conversion. If running kilosort from GUI, set both the working directory and the final output directory to kiloSorted_MNAME, such that both "rez.mat" and "temp_wh.dat" files are written out to the same directory. The former contains spike times and the latter contains waveforms, both of which are needed for visualization by Plexon Offline Sorter.

3. Click kilo2plexon.bat to write out toPlexonOfflineSorter_MNAME/sessionXX/subsessionZ/sessionXX.mat. It converts waveforms in "temp_wh.dat" (which is in the Phy format) to a format readable by Plexon Offline Sorter.

4. Start Plexon Offline Sorter. Go to File -> Import -> Spike Data from MATLAB and open toPlexonOfflineSorter_MNAME/sessionXX/subsessionZ/sessionXX.mat files.

  a. Check "Import unit designation", select a designation. Usually, there's only one choice.

  b. "Time units" should be set to seconds.

  c. Set "digitizing frequency" to the proper value (such as 30000 Hz). You can check it in "rez.mat" file's "opt" variable.

  Once open by Plexon Offline Sorter, do manual sorting if necessary. You can skip the offline sorting procedure, if you think automatic sorting was good enough.

5. In Plexon Offline Sorter, go to File -> Export Per-waveform Data. Select "Matlab file" as Format.     

    a. Choose All Channels, All Units, One file per channel.

    c. Removing check marks from PC1 and PC2 can save some disk space.

    d. Sometimes, an error message shows up saying "the file is already opened by Microsoft Excel". In that case, make a new directory and write out there. Then you have to move written-out files to the originally intended directory.

    e. You can write out to toPlexonOfflineSorter_MNAME/sessionXX/subsessionZ/sessionXX.mat, which is the same directory as the input directory.

    f. The output files are "sessionXX_YYY.mat" where "_YYY" indicate channel numbers. Each of this file contains wvf0 (matrix).

6. Click plexon2stability.bat. It reads toPlexonOfflineSorter_MNAME/sessionXX/subsessionZ/sessionXX_YYY.mat and write out "sessionXX_elYY_subsessZ_single_channel_sort.mat" into the directory, matrixNotCellArray/sessionXX.

7. Click divide_by_channel.bat. It generates matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat for each single unit (channel). The mat files contain variables wvf_single_channel and times_single_channel.

8. From Matlab, execute sortpipe/convert_to_1x1_cell_array.m. It does the following conversions to variables in matrixNotCellArray_MNAME/sessionXX/sessionXX_elYY_subsessZ_single_channel.mat and write out to forStabilityAnalysis_MNAME.

    a. wvf_single_channel (matrix) ->  wvf (1x1 cell array)

    b. times_single_channel -> times (1x1 cell array), then save them in sessionXX_elYY_subsessZ.mat. Also convert wvfY (matrix) in forStabilityAnalysis/sessionXX/sessionXX_elYY_subsessZ_single_channel_sort.mat to wvf (1x1 cell array).

9. Click copy_behavior.bat. It copies behavioral data (EDfiles and Info) in behavior_dir (for example Z:\\prut.lab\\MNAME_DAQ or ../../data/MNAME) to forStabilityAnalysis//sessionXX. It also generates three directories elc_01plx, EDfiles, and Info in D:\\forStabilityAnalysis/sessionXX.

10. From Matlab, execute sortUtils\\MergePlx2EDs to merge spike trains and behavioral data. The output will be in the directory, plxMergeEDfiles.

11. Merge data by executing the following commands on a command line interface. The lines generate forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles. The final "\\" in the first argument is required.

```
cd D:\\MNAME_programs_updated\\sortUtils
MergePlx2EDs('D:\\forStabilityAnalysis_MNAME\\', 'n300122');
```

12. From Matlab, execute the stability analysis program GUI, read forStabilityAnalysis_MNAME\\sessionXX\\plxMergeEDfiles, and do stability analysis.
