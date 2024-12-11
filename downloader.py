import os
from loguru import logger
import requests
import geopandas as gpd
import hydra
from omegaconf import OmegaConf

class Downloader():
    """
    Class to download geoboundary files from www.geoboundaries.org/
    """

    def __init__(self, link, output_dir):
        """
        Initializes the Downloader object.

        Parameters
        ----------
        output_dir : str
            Directory to save the downloaded files
        link : dict
            Dictionary containing the download link and metadata of a geoboundary file
        """
        self.output_dir = output_dir
        self.link = link

    def save_to_path(self, iso, data_url, path, level):
        """Transforms .geojson from data_url and saves .shp to the specified path.

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
        data_url = self.link['url']
        level = self.link['level']
        iso = self.link['iso']

        path = self.output_dir + '/' + iso + '_' + level + '/'
        
        os.makedirs(path, exist_ok=True)

        # try 4 times in case of intermittent issues
        for i in range(4):
            try:
                self.save_to_path(
                    iso, data_url, path, level)
                err = None
                break
            except Exception as e:
                logger.error(f'Download {iso} {level} failed attempt %d' % (i+1))
                err = e

        return err

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg):
    errors = {}  # will map download name to error message if any 

    for link in cfg.links:
        ##make an omega conf object a dictionary
        link=OmegaConf.to_container(link, resolve=True)

        downloader = Downloader(
            output_dir=cfg.output_dir,
            link=link, #link is a dictionary as required by the Downloader class
            )
        
        errors[link["iso"] + "_" + link["level"]] = (downloader.download())
    
    for suffix, error in errors.items():
        if error:
            logger.error(f'Error in download {suffix}: {error}')

if __name__ == "__main__":
    main()