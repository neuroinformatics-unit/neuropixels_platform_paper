# %%
import pandas as pd
import os
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm

from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# Example cache directory path, it determines where downloaded data will be stored
output_dir = '/Users/lauraporta/local1/ecephys_cache_dir/'

# this path determines where downloaded data will be stored
manifest_path = os.path.join(output_dir, "manifest.json")
cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)
print(cache.get_all_session_types())

sessions = cache.get_session_table()
brain_observatory_type_sessions = sessions[sessions["session_type"] == "brain_observatory_1.1"]
brain_observatory_type_sessions.tail()

#  read table with layer infortmation
df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'unit_table.csv'), low_memory=False)


# %%
layers = [1, 2, 3, 4, 5, 6]
time_step = 0.01
time_bins = np.arange(-0.1, 2 + time_step, time_step)

# %%
layer_data = {
    "VSIp_1": [],
    "VSIp_2": [],
    "VSIp_3": [],
    "VSIp_4": [],
    "VSIp_5": [],
    "VSIp_6": [],
    "LGd": []
}

for session_id in brain_observatory_type_sessions.index.unique():
    try:
        print("Collecting data for session: ", session_id)
        session = cache.get_session_data(session_id)

        session_unit_table = df[df.ecephys_session_id == session_id]

        print("Filtering units...")
        VISp_units = session.units[session.units["ecephys_structure_acronym"] == 'VISp']
        VISp_units_table = session_unit_table[session_unit_table.area == 'VISp']

        presentations = session.get_stimulus_table("flashes")

        for layer in layers:
            print(f"Preparing data for layer {layer}...")
            this_layer_units_table = VISp_units_table[VISp_units_table.cortical_layer == layer]
            units = this_layer_units_table.ecephys_unit_id

            units_data = VISp_units[VISp_units.index.isin(units)]

            if len(units_data) == 0:
                print(f"No units found for layer {layer} in session {session_id}")
            else:
                print("Preparing plot...")

                histograms = session.presentationwise_spike_counts(
                    stimulus_presentation_ids=presentations.index.values,  
                    bin_edges=time_bins,
                    unit_ids=units_data.index.values
                )

                print(histograms.coords)

                mean_histograms = histograms.mean(dim="stimulus_presentation_id")

                print("Plotting...")
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pcolormesh(
                    mean_histograms["time_relative_to_stimulus_onset"], 
                    np.arange(mean_histograms["unit_id"].size),
                    mean_histograms.T, 
                    vmin=0,
                    vmax=1
                )

                #  plot the sum of the mean histograms as a line plot on top of the pcolormesh
                sum_histograms = mean_histograms.sum(dim="unit_id")
                ax.plot(
                    mean_histograms["time_relative_to_stimulus_onset"], 
                    sum_histograms, 
                    color="red"
                )
                ax.set_ylabel("unit", fontsize=24)
                ax.set_xlabel("time relative to stimulus onset (s)", fontsize=24)
                ax.set_title(f"Layer {layer} - session {session_id}, flashes", fontsize=24)
                # plt.show()

                # save figure
                fig.savefig(f"figures/peristimulus_time_histograms_layer_{layer}_session_{session_id}.png")
                plt.close(fig)

                layer_data[f"VSIp_{layer}"].append(mean_histograms)

            LGd_units = session.units[session.units["ecephys_structure_acronym"] == 'LGd']
            LGd_units_table = session_unit_table[session_unit_table.area == 'LGd']

            presentations = session.get_stimulus_table("flashes")

            #  no layers in thalamus
            print("Preparing data for LGd...")
            this_layer_units_table = LGd_units_table

            units = this_layer_units_table.ecephys_unit_id

            units_data = LGd_units[LGd_units.index.isin(units)]

            if len(units_data) == 0:
                print(f"No units found for LGd in session {session_id}")
            else:
                print("Preparing plot...")

                histograms = session.presentationwise_spike_counts(
                    stimulus_presentation_ids=presentations.index.values,  
                    bin_edges=time_bins,
                    unit_ids=units_data.index.values
                )

                print(histograms.coords)

                mean_histograms = histograms.mean(dim="stimulus_presentation_id")

                print("Plotting...")
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pcolormesh(
                    mean_histograms["time_relative_to_stimulus_onset"], 
                    np.arange(mean_histograms["unit_id"].size),
                    mean_histograms.T, 
                    vmin=0,
                    vmax=1
                )

                #  plot the sum of the mean histograms as a line plot on top of the pcolormesh
                sum_histograms = mean_histograms.sum(dim="unit_id")
                ax.plot(
                    mean_histograms["time_relative_to_stimulus_onset"], 
                    sum_histograms, 
                    color="red"
                )

                ax.set_ylabel("unit", fontsize=24)
                ax.set_xlabel("time relative to stimulus onset (s)", fontsize=24)
                ax.set_title(f"LGd - session {session_id}, flashes", fontsize=24)
                # plt.show()

                # save figure
                fig.savefig(f"figures/peristimulus_time_histograms_LGd_session_{session_id}.png")
                plt.close(fig)
                
                layer_data["LGd"].append(mean_histograms)

    except Exception as e:
        print(f"Error processing session {session_id}: {e}")
        continue

# %%
# plot the activity of the units in each layer across all sessions

for layer, data in layer_data.items():
    if len(data) == 0:
        print(f"No data found for layer {layer}")
    else:
        print(f"Plotting data for layer {layer}...")
        mean_data = np.mean(data, axis=0)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pcolormesh(
            mean_data["time_relative_to_stimulus_onset"], 
            np.arange(mean_data["unit_id"].size),
            mean_data.T, 
            vmin=0,
            vmax=1
        )

        ax.set_ylabel("unit", fontsize=24)
        ax.set_xlabel("time relative to stimulus onset (s)", fontsize=24)
        ax.set_title(f"{layer} - flashes", fontsize=24)
        # plt.show()

        # save figure
        fig.savefig(f"figures/peristimulus_time_histograms_{layer}_flashes.png")
        plt.close(fig)