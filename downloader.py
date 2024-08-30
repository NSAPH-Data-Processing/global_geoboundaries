import os

from loguru import logger
import requests
import yaml
import geopandas as gpd


class Downloader():

    def __init__(self, output_dir, config_dir=None, overwrite=False, dry_run=False):
        self.output_dir = output_dir
        self.config_dir = config_dir
        self.overwrite = overwrite
        self.dry_run = dry_run

    def save_to_path(self, iso, data_url, path, suffix):
        """Saves the .geojson from data_url to the specified path.

        Parameters
        ----------
        iso : str

        data_url : str
            URL of .geojson file

        path : str
            Local path to which to save the contents of data_url

        suffix : int
            e.g. 0, 1, 2
        """
        if self.dry_run:
            logger.warning(
                f'Dry run: Downloading {iso} ADM{suffix} file from {data_url}')
            return

        logger.info(f"Downloading {iso} ADM{suffix} file from {data_url}")

        response = requests.get(data_url)

        if response.status_code == 200:
            gdf = gpd.read_file(response.text)
            outfilename = iso + '_ADM' + str(suffix) + '.shp'
            logger.info(f"Saving file to {path + outfilename}")

            gdf.to_file(os.path.join(path, outfilename))
        else:
            logger.error(f'Response status code: {response.status_code}')
            raise ValueError(f'Could not download data from URL: {data_url}')


    def get_iso_config_from_dir(self, iso):
        # Return the full parsed iso config from file.
        config_path = os.path.join(self.config_dir, '%s.yaml' % iso.upper())
        if not os.path.exists(config_path):
            return None

        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert config['iso'] == iso.upper()
        return config


    # returns a dictionary of downloads to error messages, if any
    def download(self, iso):
        # extract iso config
        try:
            full_iso_config = self.get_iso_config_from_dir(iso)
        except Exception as err:
            logger.error(f'Error getting config for {iso}: {err}')
            return {iso: f'Error getting config for {iso}: check config for errors'}

        if full_iso_config is None:
            logger.info(f'No existing config for {iso}')
            return

        errors = {}  # will map download name to error message if any

        # do this for all iso downloads
        for iso_config in full_iso_config['links']:
            suffix = iso_config['level']
            data_url = iso_config['link']
            path = self.output_dir + iso + '_ADM' + str(suffix) + '/'
            
            if not self.overwrite and os.path.exists(path):
                logger.info(f'Directory for {iso} exists, skipping download. To overwrite, specify --overwrite.')
                return errors
            
            os.makedirs(path, exist_ok=True)

            # try 4 times in case of intermittent issues
            err = None
            for i in range(4):
                try:
                    self.save_to_path(
                        iso, data_url, path, suffix)
                    err = None
                    break
                except Exception as e:
                    logger.error(f'Download {iso} {suffix} failed attempt %d' % (i+1))
                    err = e

            if err:
                errors[suffix] = err

        return errors