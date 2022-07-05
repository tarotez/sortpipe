import numpy as np
from phy.apps import WaveformMixin
from phy.apps.template import TemplateController
from phy.apps.base import RawDataFilter
from phylib.io.model import TemplateModel
from phy.utils.context import Context

class SimpleController(TemplateController, WaveformMixin):
    def __init__(self, dir_path, dat_path, sample_rate, n_channels_dat, **kwargs):
        self.model = TemplateModel(dir_path=dir_path, dat_path=dat_path, sample_rate=sample_rate, 
                                   n_channels_dat=n_channels_dat, **kwargs)
        self.raw_data_filter = RawDataFilter()
        # the main modification from the original TemplateController and BaseContoller in Phy is 
        # in commenting out the following line, to avoid an error during filtering that says 
        # the value of Wn is out of range.
        ### self.raw_data_filter.add_default_filter(self.model.sample_rate)        
        self._set_cluster_metrics()
        self._set_similarity_functions()        
        self.context = Context(dir_path)        
        self._set_supervisor()
        self.n_chunks_kept = 20
        self._set_selector()
        self.default_show_mapped_channels = True

    #--------------------------
    # the only difference from the original _get_waveforms_with_n_spikes() is that it 
    # returns spike_ids also, not only waveforms: Bunch.
    def _get_waveforms_with_n_spikes(
            self, cluster_id, n_spikes_waveforms, current_filter=None):

        # HACK: we pass self.raw_data_filter.current_filter so that it is cached properly.
        pos = self.model.channel_positions

        # Only keep spikes from the spike waveforms selection.
        if self.model.spike_waveforms is not None:
            subset_spikes = self.model.spike_waveforms.spike_ids
            spike_ids = self.selector(
                n_spikes_waveforms, [cluster_id], subset_spikes=subset_spikes)
        # Or keep spikes from a subset of the chunks for performance reasons (decompression will
        # happen on the fly here).
        else:
            spike_ids = self.selector(n_spikes_waveforms, [cluster_id], subset_chunks=True)

        # Get the best channels.
        channel_ids = self.get_best_channels(cluster_id)
        channel_labels = self._get_channel_labels(channel_ids)

        # Load the waveforms, either from the raw data directly, or from the _phy_spikes* files.
        data = self.model.get_waveforms(spike_ids, channel_ids)
        if data is not None:
            data = data - np.median(data, axis=1)[:, np.newaxis, :]
        assert data.ndim == 3  # n_spikes, n_samples, n_channels

        # Filter the waveforms.
        if data is not None:
            data = self.raw_data_filter.apply(data, axis=1)
        return Bunch(
            data=data,
            channel_ids=channel_ids,
            channel_labels=channel_labels,
            channel_positions=pos[channel_ids],
        ), spike_ids


# reorganize (sort) waveforms and spike_times by channels (i.e electrodes).
# units_byc[channel_id]: a map from spike to cluster (i.e. unit).
def reorganize_by_prim_elec(waveformsL, times, spike_idsL, prim_elecL):
    n_channels = max(prim_elecL) + 1
    n_samples = waveformsL[0].shape[1]
    wvf_byc = [np.zeros((0, n_samples)) for _ in range(n_channels)]
    times_byc = [np.zeros((0), dtype=int)[np.newaxis].transpose() for _ in range(n_channels)]
    units_byc = [np.zeros((0), dtype=np.int16)[np.newaxis].transpose() for _ in range(n_channels)]
    for cluster_id, (waveforms, spike_ids, prim_elec) in enumerate(zip(waveformsL, spike_idsL, prim_elecL)):        
        # print(cluster_id, "", waveforms.shape, "", prim_elec)
        wvf_byc[prim_elec] = np.concatenate((wvf_byc[prim_elec], waveforms), axis=0)
        spike_num = waveforms.shape[0]
        if spike_num > 0:            
            times_segment = times[spike_ids,0]
            # print('len(times_segment) =', len(times_segment))
            times_byc[prim_elec] = np.concatenate((times_byc[prim_elec], times_segment[np.newaxis].transpose()), axis=0)
            units_byc[prim_elec] = np.concatenate((units_byc[prim_elec], np.array([cluster_id] * spike_num, dtype=np.int16)[np.newaxis].transpose()), axis=0)                    
    return wvf_byc, times_byc, units_byc