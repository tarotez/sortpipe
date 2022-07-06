import numpy as np

#----------------------------------------------------------------------------
# reorganize (sort) waveforms and spike_times by channels (i.e electrodes).
# units_byc[channel_id]: a map from spike to cluster (i.e. unit).
def reorganize_by_prim_elec(waveformsL, times, spike_idsL, prim_elecL):
    n_channels = max(prim_elecL) + 1
    n_samples = waveformsL[0].shape[1]
    wvf_byc = [np.zeros((0, n_samples)) for _ in range(n_channels)]
    # setting the elements of times_byc and units_byc to be in the 2-D array shape that will be converted to Matlab matrices
    times_byc = [np.zeros((0), dtype=np.double)[np.newaxis].transpose() for _ in range(n_channels)]
    units_byc = [np.zeros((0), dtype=np.int16)[np.newaxis].transpose() for _ in range(n_channels)]
    for cluster_id, (waveforms, spike_ids, prim_elec) in enumerate(zip(waveformsL, spike_idsL, prim_elecL)):        
        # print(cluster_id, "", waveforms.shape, "", prim_elec)
        wvf_byc[prim_elec] = np.concatenate((wvf_byc[prim_elec], waveforms), axis=0)
        spike_num = waveforms.shape[0]
        if spike_num > 0:            
            times_segment = times[spike_ids,0]
            # print('len(times_segment) =', len(times_segment))
            # setting the elements of times_byc and units_byc to be in the 2-D array shape that will be converted to Matlab matrices
            times_byc[prim_elec] = np.concatenate((times_byc[prim_elec], times_segment[np.newaxis].transpose()), axis=0)
            units_byc[prim_elec] = np.concatenate((units_byc[prim_elec], np.array([cluster_id] * spike_num, dtype=np.int16)[np.newaxis].transpose()), axis=0)
    return wvf_byc, times_byc, units_byc

#----------------------------------------------------------------------------
# renumber unit_ids so it starts from 1 for all channels.
def renumber_unit_ids_from_global_to_local(units_byc):
    units_byc_renum = [np.zeros((0), dtype=np.int16)[np.newaxis].transpose() for _ in range(len(units_byc))]
    for channel_id, units in enumerate(units_byc):
        unique_units = []
        for unit in units:
            if not unit[0] in unique_units:
                unique_units.append(unit[0])
        g2l = dict()
        for local_id, global_id in enumerate(unique_units, start=1):
            g2l[global_id] = np.int16(local_id)
        renum = list(map(lambda x: [g2l[x[0]]], units))
        # setting the elements of units_byc_renum to be in the 2-D array shape that will be converted to Matlab matrices
        if len(renum) > 0:
            units_byc_renum[channel_id] = np.array(renum, dtype=np.int16)
        # print('for channel_id', channel_id, ' units_byc_renum[channel_id].shape =', units_byc_renum[channel_id].shape)
        
    return units_byc_renum