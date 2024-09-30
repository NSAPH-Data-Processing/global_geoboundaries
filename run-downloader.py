""" Main script to run downloads of country shapefiles. """

import os
import sys

from loguru import logger

from args import parser as download_parser
from downloader import Downloader
import pycountry

from omegaconf import DictConfig, OmegaConf
import hydra

_ALL_ISO = [c.alpha_3 for c in pycountry.countries]


def iso_from_args(args):
    # if isos are user-specified, download only those
    if args.iso:
        logger.info(f'Downloading iso(s) {args.iso}')
        return args.iso.split(',')
    else:
        logger.info('Downloading all isos')
        return _ALL_ISO


# def config_dir_from_args(args):
#     if args.iso_urls:
#         subdir = 'ISO'
#     elif args.adm_urls:
#         subdir = 'ADM'

    return os.path.join(os.path.dirname(__file__), 'configs', subdir)

# Return a small string describing which run this is.
def run_type_from_args(args):
    if args.iso_urls:
        return 'ISO'
    elif args.adm_urls:
        return 'ADM'
    raise ValueError('no run type specified in args: %s' % args)

@hydra.main(config_path="conf", config_name="config", version_base=None)
def main(cfg):
    # if args_list is None:
    #     args_list = sys.argv[1:]
    # args = download_parser.parse_args(args_list)
    
    # config_dir = config_dir_from_args(args)
    downloader = Downloader(
        output_dir=cfg.output_dir,
        dry_run=cfg.dry_run, overwrite=cfg.overwrite, config_dir=cfg)

    failed_isos = []

    for iso in iso_from_args(cfg.iso):
        errors = downloader.download(iso)
        if errors is None:
            continue
        for suffix, error in errors.items():
            logger.error(f'Error in {iso} {suffix}: {error}')
            failed_isos.append((iso, str(suffix)))

    if failed_isos:
        failed_isos_str = ', '.join([':'.join(x) for x in failed_isos])
        logger.error(f"Errored download isos for this run: {failed_isos_str}")
    else:
        logger.info("All attempted ISOs successfully downloaded")


if __name__ == "__main__":
    main()