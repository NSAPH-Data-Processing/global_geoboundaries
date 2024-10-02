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


    # def get_iso_config_from_dir(self, iso):
    #     # Return the full parsed iso config from file.
    #     print("\n\nconfig path:", self.config_dir)
       
    #     # if one of ADM0, AMD1, .... then
    #     #special case for ISOs

    #     import pdb; pdb.set_trace()
    #     # config_path = os.path.join(self.config_dir.geoboundaries, '%s.yaml' % iso.upper())
    #     # print("config path:", self.config_dir)

    #     config_dict = next((item for item in self.config_dir.geoboundaries['links'] if item['iso'] == iso), None)


    #     # if not os.path.exists(config_path):
    #     #     return None

    #     # with open(config_path) as f:
    #     #     config = yaml.safe_load(f)
        
    #     # c = config['iso' == iso.upper()]

    #     # assert config['iso'] == iso.upper()
    #     return config_dict

     # returns a dictionary of downloads to error messages, if any
    def download(self):
        errors = {}  # will map download name to error message if any
        # do this for all iso downloads
        for iso_config in self.config_dir.geoboundaries['links']:
            # suffix = iso_config['level']
            data_url = iso_config['link']
            iso = iso_config['iso']
            level = self.config_dir.geoboundaries['adm']                
            path = self.output_dir + iso + '_' + self.config_dir.geoboundaries['adm'] + '/'
            
            if not self.overwrite and os.path.exists(path):
                logger.info(f'Directory for {iso} exists, skipping download. To overwrite, specify \'overwrite: True\' in the config.')
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