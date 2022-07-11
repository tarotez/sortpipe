
import numpy as np
from lib.simple_controller import SimpleController
from lib.transform_data_structure import reorganize_by_prim_elec, renumber_unit_ids_from_global_to_local

def convert(dir_path, sample_rate, n_electrodes, sep):

    dat_path = dir_path + sep + 'temp_wh.dat'   # kilosort outputs waveforms into temp_wh.dat in the working directory
    # channel_map = np.load(dir_path + sep + 'channel_map.npy')
    spike_clusters = np.load(dir_path + sep + 'spike_clusters.npy')
    spike_times = np.single(np.load(dir_path + sep + 'spike_times.npy'))
    n_clusters = len(np.unique(spike_clusters))

    sc = SimpleController(dir_path, dat_path, sample_rate, n_electrodes)
    sc.n_spikes_waveforms = len(spike_times)  # maximum number of spikes to retrieve from one unit

    # get waveforms, spike_ids, and primary_electrodes for all clusters.
    channel_rank = 0  # set to 0 for the primary channel, i.e. the electrode that contributed most in finding the unit.
    waveformsL = []
    spike_idsL = []
    primary_electrodeL = []   # map: cluster_id -> channel_id
    # print('original number of clusters:', n_clusters)    
    for cluster_id in range(n_clusters):
        try:
            waveforms, spike_ids = sc._get_waveforms(cluster_id)
            waveformsL.append(waveforms.data[:,:,channel_rank])
            spike_idsL.append(spike_ids)
            primary_electrodeL.append(waveforms.channel_ids[0])
        except:
            # print('cluster', cluster_id, 'missing.')
            pass

    wvf_byc, times_byc, units_byc = reorganize_by_prim_elec(waveformsL, spike_times, spike_idsL, primary_electrodeL)
    units_byc = renumber_unit_ids_from_global_to_local(units_byc)

    # change 1-D numpy array into matlab matrices (2-D).
    wvf_t = np.array(wvf_byc, dtype=object)[np.newaxis].transpose()
    times_t = np.array(times_byc, dtype=object)[np.newaxis].transpose() / sample_rate
    # print('units_byc =')
    # print(units_byc)
    # print('np.array(units_byc, dtype=object).shape =', np.array(units_byc, dtype=object).shape)
    units_t = np.array(units_byc, dtype=object)[np.newaxis].transpose()

    return dict(times=times_t, wvf=wvf_t, units=units_t)