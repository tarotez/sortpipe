import numpy as np
from scipy.io import savemat
from lib.kilo2plex import SimpleController, reorganize_by_prim_elec
from phylib.utils._types import Bunch

# dir_path = '../../kiloout_220626'   # output directory of kilosort
dir_path = '../../kiloSorted_Nana32/n100122/s1'
dat_path = dir_path + '/temp_wh.dat'   # signal file produced by kilosort to the working directory
sample_rate = 30000   # sampling rate used by the electrodes
n_channels_dat = 32   # number of electrodes
channel_rank = 0  # set to 0 for the primary channel, i.e. the electrode that contributed most in finding the unit.

channel_map = np.load(dir_path + '/channel_map.npy')
spike_clusters = np.load(dir_path + '/spike_clusters.npy')
spike_times = np.load(dir_path + '/spike_times.npy')
n_channels = channel_map.shape[1]
n_clusters = len(np.unique(spike_clusters))

max_spike_num_per_unit = len(spike_times)  # maximum number of spikes to retrieve from one unit

sc = SimpleController(dir_path, dat_path, sample_rate, n_channels_dat)
sc.n_spikes_waveforms = max_spike_num_per_unit


# get waveforms, spike_ids, and primary_electrodes for all clusters.
waveformsL = []
spike_idsL = []
primary_electrodeL = []   # map: cluster_id -> channel_id
for cluster_id in range(n_clusters):
    try:
        waveforms, spike_ids = sc._get_waveforms(cluster_id)
        waveformsL.append(waveforms.data[:,:,channel_rank])
        spike_idsL.append(spike_ids)
        primary_electrodeL.append(waveforms.channel_ids[0])
    except:
        print('cluster', cluster_id, 'missing.')

