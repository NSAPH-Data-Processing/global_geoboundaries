import os

from loguru import logger
import requests
import yaml
import geopandas as gpd

from hydra.core.hydra_config import HydraConfig
import hydra

class Downloader():

    def __init__(self, output_dir, config_dir=None, overwrite=False, dry_run=False):
        self.output_dir = output_dir
        self.config_dir = config_dir
        self.overwrite = overwrite
        self.dry_run = dry_run

    def save_to_path(self, iso, data_url, path, level):
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
                f'Dry run: Downloading {iso} {level} file from {data_url}')
            return

        logger.info(f"Downloading {iso} {level} file from {data_url}")

        response = requests.get(data_url)

        if response.status_code == 200:
            gdf = gpd.read_file(response.text)
            outfilename = iso + '_' + str(level) + '.shp'
            logger.info(f"Saving file to {path + outfilename}")

            gdf.to_file(os.path.join(path, outfilename))
        else:
            logger.error(f'Response status code: {response.status_code}')
            raise ValueError(f'Could not download data from URL: {data_url}')

     # returns a dictionary of downloads to error messages, if any
    def download(self):
        errors = {}  # will map download name to error message if any        
        
        for link_config in self.config_dir.geoboundaries['links']:
            data_url = link_config['link']
            if 'level' in link_config: #iso config
                level = 'ADM' + str(link_config['level'])
                iso = self.config_dir.geoboundaries['iso']
            else:
                level = self.config_dir.geoboundaries['adm']
                iso = link_config['iso']

            path = self.output_dir + iso + '_' + level + '/'
            
            if not self.overwrite and os.path.exists(path):
                logger.info(f'Directory for {iso} exists at {path}, skipping download. To overwrite, specify \'overwrite: True\' in the config.')
                continue
            
            os.makedirs(path, exist_ok=True)

            # try 4 times in case of intermittent issues
            err = None
            for i in range(4):
                try:
                    self.save_to_path(
                        iso, data_url, path, level)
                    err = None
                    break
                except Exception as e:
                    logger.error(f'Download {iso} {level} failed attempt %d' % (i+1))
                    err = e

            if err:
                errors[level] = err

        return errors
    
@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg):
    downloader = Downloader(
        output_dir=cfg.output_dir,
        dry_run=cfg.dry_run, overwrite=cfg.overwrite, config_dir=cfg)
    
    errors = downloader.download()
    for suffix, error in errors.items():
        logger.error(f'Error in level {suffix}: {error}')


if __name__ == "__main__":
    main()