import numpy as np
from phy.apps import WaveformMixin
from phy.apps.template import TemplateController
from phy.apps.base import RawDataFilter
from phylib.io.model import TemplateModel
from phy.utils.context import Context
from phylib.utils._types import Bunch

#----------------------------------------------------------------------------
# overrides __init__() of TemplateController in Phy (spike visualization tool).
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
    # returns spike_ids also, not only waveforms.
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
