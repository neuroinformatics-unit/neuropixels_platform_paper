# Neuropixels Platform Paper

<img src="icon.png" width="400">

This repository contains code for generating the figures in the pre-print describing the scientific findings from the Allen Institute's [Neuropixels data collection platform](https://portal.brain-map.org/explore/circuits/visual-coding-neuropixels).

Most of the figures can be generated from publicly available NWB files and unit tables, available via the AllenSDK. See [the AllenSDK documentation](https://allensdk.readthedocs.io/en/latest/visual_coding_neuropixels.html) for an overview of the dataset and example notebooks for accessing it.

Each figure in the pre-print has a folder with associated code. Data required for figure generation that's not available in the October 2019 release (e.g., from the change detection experiments) is included in the `data` directory.

This repository is still a work in progress; we will continue to clean up the code and add documentation throughout the review process.


## Level of Support

We are not currently supporting this code, but simply releasing it to the community AS IS.  We are not able to provide any guarantees of support. The community is welcome to submit issues, but you should not expect an active response.


## Terms of Use

See [Allen Institute Terms of Use](https://alleninstitute.org/legal/terms-use/)


© 2019 Allen Institute for Brain Science

# Run the additional scripts
Create an environment via the environment.yml file:
```bash
conda env create -f environment.yml
conda activate neuropixels_platform_paper_test
```

Then, edit the PATH VARIABLES in the `common/paths.py` file to point to the correct directories on your machine.
If you do not have a `ecephys_cache_dir` please create one.
Then run the file to create the units table, which contains layer information for each unit:
```bash
python common/create_units_table.py
```

Now you can run `generate_figures_for_each_layer.py` to generate the figures for each layer. N.B. this script will take a long time to run the first time, as it will download the necessary data from the Allen Institute's servers. Please edit the PATH VARIABLES in the `common/paths.py` file to point to the correct directories on your machine as before.
```bash
python generate_figures_for_each_layer.py
```

