import numpy as np
# from lib.manage_params import read_config

#----------------------------------------------------------------------------
# reorganize (sort) waveforms and spike_times by channels (i.e electrodes).
# units_byc[channel_id]: a map from spike to cluster (i.e. unit).
# def reorganize_times_by_prim_elec(times, spike_idsL, prim_elecL, n_electrodes):
#     # setting the elements of times_byc and units_byc to be in the 2-D array shape that will be converted to Matlab matrices
#     times_byc = [np.zeros((0), dtype=np.double)[np.newaxis].transpose() for _ in range(n_electrodes)]
#     units_byc = [np.zeros((0), dtype=np.int16)[np.newaxis].transpose() for _ in range(n_electrodes)]   # starts from minus one.
#     for cluster_id, (spike_ids, prim_elec) in enumerate(zip(spike_idsL, prim_elecL)):
#         # print(cluster_id, "", waveforms.shape, "", prim_elec)
#         spike_num = waveforms.shape[0]
#         if spike_num > 0:
#             times_segment = times[spike_ids,0]
#             # print('len(times_segment) =', len(times_segment))
#             # setting the elements of times_byc and units_byc to be in the 2-D array shape that will be converted to Matlab matrices
#             times_byc[prim_elec] = np.concatenate((times_byc[prim_elec], times_segment[np.newaxis].transpose()), axis=0)
#             units_byc[prim_elec] = np.concatenate((units_byc[prim_elec], np.array([cluster_id] * spike_num, dtype=np.int16)[np.newaxis].transpose()), axis=0)
#     return times_byc, units_byc

#----------------------------------------------------------------------------
# reorganize (sort) waveforms and spike_times by channels (i.e electrodes).
# units_byc[channel_id]: a map from spike to cluster (i.e. unit).
def reorganize_by_prim_elec(waveformsL, times, spike_idsL, prim_elecL, n_electrodes):
    assert len(waveformsL) > 0, 'waveformsL is empty. Check if temp_wh.dat is in the kilosorted directory.'
    n_samples = waveformsL[0].shape[1]
    wvf_byc = [np.zeros((0, n_samples)) for _ in range(n_electrodes)]
    # setting the elements of times_byc and units_byc to be in the 2-D array shape that will be converted to Matlab matrices
    times_byc = [np.zeros((0), dtype=np.double)[np.newaxis].transpose() for _ in range(n_electrodes)]
    units_byc = [np.zeros((0), dtype=np.int16)[np.newaxis].transpose() for _ in range(n_electrodes)]   # starts from minus one.
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
        unique_units = [-1]  # global ID for unsorted is -1. It should be mapped to 0 in local ID.
        for unit in units:
            if not unit[0] in unique_units:
                unique_units.append(unit[0])
        g2l = dict()
        for local_id, global_id in enumerate(unique_units,start=0):
            g2l[global_id] = np.int16(local_id)
        renum = list(map(lambda x: [g2l[x[0]]], units))
        # setting the elements of units_byc_renum to be in the 2-D array shape that will be converted to Matlab matrices
        if len(renum) > 0:
            units_byc_renum[channel_id] = np.array(renum, dtype=np.int16)
        # print('for channel_id', channel_id, ' units_byc_renum[channel_id].shape =', units_byc_renum[channel_id].shape)

    return units_byc_renum

def add_noise_unit_to_empty_channel(wvf_byc, times_byc, units_byc):
    n_electrodes = len(wvf_byc)
    n_samples = wvf_byc[0].shape[1]
    for channel_id in range(n_electrodes):
        if wvf_byc[channel_id].shape[0] == 0:
            wvf_byc[channel_id] = np.random.normal(size=(1, n_samples))
            times_byc[channel_id] = np.zeros((1), dtype=np.double)[np.newaxis].transpose()
            units_byc[channel_id] = np.zeros((1), dtype=np.int16)[np.newaxis].transpose()

    return wvf_byc, times_byc, units_byc
