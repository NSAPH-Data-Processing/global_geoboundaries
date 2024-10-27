import hydra
from omegaconf import OmegaConf
import json

conda: "environment.yaml"

with hydra.initialize(config_path="conf", version_base=None):
    cfg = hydra.compose(config_name="config", overrides=[])
    #print(OmegaConf.to_yaml(cfg))

geoboundaries_cfg = OmegaConf.to_container(cfg.geoboundaries, resolve=True) 
#print(geoboundaries_cfg)
geoboundaries_cfg_dict = {geoboundary["iso"] + "_" + geoboundary["level"]: "[" + json.dumps(geoboundary).replace('"', '') + "]" for geoboundary in geoboundaries_cfg}
print(geoboundaries_cfg_dict)
geoboundaries_list = list(geoboundaries_cfg_dict.keys())
#print(geoboundaries_list)

rule all:
    input:
        expand(
            f"{cfg.output_dir}/{{geoboundary}}/{{geoboundary}}.shp",
            geoboundary=geoboundaries_list
        )

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
        #python downloader.py "+links=[{iso: ASM, level: ADM0, boundary_year: 2021, url: https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/ASM/ADM0/geoBoundaries-ASM-ADM0.geojson}]"

# snakemake debugging commands:
# snakemake -n
# snakemake -n -p