# Geoboundaries

This project downloads country shapefiles from [geoBoundaries](https://www.geoboundaries.org/), a project of the [William and Mary GeoLab](https://sites.google.com/view/wmgeolab/). The user may either specify countries to download shapefiles for, or else administrative levels to download.

## Usage
```
Modify the arguments in the config at conf/config.yaml to change behavior.

defaults:
  - _self_
  - geoboundaries: ADM0 # possible options are ADM0-ADM5, all ISO codes

output_dir: output/

overwrite: False # whether you want to potentially overwrite previous downloads

dry_run: False # to test functionality without downloading anything
```

From the main folder, run the following:
```
python downloader.py
```

When run on all countries, e.g. by running on ADM0, ADM1, ADM2, ADM3, ADM4, and ADM5 the resulting output should be a comprehensive directory of global shapefiles that can be used for geospatial analysis.

<img width="1433" alt="Map of the world created using shapefiles downloaded by this project" src="https://github.com/user-attachments/assets/3699c16b-ce8a-4bdd-82c8-93fec04c939b">
