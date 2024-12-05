import hydra
from omegaconf import OmegaConf
import json

conda: "environment.yaml"

# Hydra initialization
with hydra.initialize(config_path="conf", version_base=None):
    cfg = hydra.compose(config_name="config", overrides=[])

# uses OmegaConf to parse geoboundary configs
geoboundaries_cfg = OmegaConf.to_container(cfg.geoboundaries, resolve=True) 

# creates a dictionary of all geoboundary configs
geoboundaries_cfg_dict = {geoboundary["iso"] + "_" + geoboundary["level"]: "[" + json.dumps(geoboundary).replace('"', '') + "]" for geoboundary in geoboundaries_cfg}

# this grabs a list of all the countries from the geoboundary config dictionary
geoboundaries_list = list(geoboundaries_cfg_dict.keys())

# the following ensures that geoboundaries for all countries in the geoboundaries_list are accounted for
rule all:
    input:
        expand(
            f"{cfg.output_dir}/{{geoboundary}}/{{geoboundary}}.shp",
            geoboundary=geoboundaries_list
        )

# this is the meat of the operation: it downloads the geoboundaires sequentially and creates each folder folders
rule download_geoboundaries:
    output:
        f"{cfg.output_dir}/{{geoboundary}}/{{geoboundary}}.shp"
    params:
        links = lambda wildcards: geoboundaries_cfg_dict[wildcards.geoboundary]
    shell:
        f"""
        echo {{wildcards.geoboundary}}
        python downloader.py "+links={{params.links}}"
        """
