# Geoboundaries

This project downloads country shapefiles from [geoBoundaries](https://www.geoboundaries.org/), a project of the [William and Mary GeoLab](https://sites.google.com/view/wmgeolab/). The user may either specify countries to download shapefiles for, or else administrative levels to download.

## Usage
```
run-downloader.py [-h] [--output_dir OUTPUT_DIR] [--iso ISO] [--dry-run] [--overwrite] (--download-by-isos | --download-by-adm)

 CLI argument definitions for the downloader. This module defines the argument parser. 

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Output directory for downloads
  --iso ISO             Comma-separated list of iso 3-letter codes. If present, will only download those.
  --dry-run             If present, will only print the request and do nothing
  --overwrite           Overwrite previous runs
  --download-by-isos    Download shapefiles by ISO
  --download-by-adm     Download shapefiles by admin level
```

When run on all countries, the resulting output should be a directory of shapefiles that can be used for geospatial analysis.

<img width="1433" alt="Map of the world created using shapefiles downloaded by this project" src="https://github.com/user-attachments/assets/3699c16b-ce8a-4bdd-82c8-93fec04c939b">
