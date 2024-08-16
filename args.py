""" CLI argument definitions for the downloader. This module defines the argument parser. """

from argparse import ArgumentParser, RawDescriptionHelpFormatter


parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawDescriptionHelpFormatter)

parser.add_argument(
    '--output_dir',
    help='Output directory for downloads')

parser.add_argument('--iso',
    default='',
    help='Comma-separated list of iso 3-letter codes. If present, will only download those.')

parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False,
    help='If present, will only print the request and do nothing')

parser.add_argument('--overwrite', dest='overwrite', action='store_true', default=False,
    help='Overwrite previous runs')

# Determines which downloads we're aiming to make. Only one can be true at a time
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--download-by-isos', dest='iso_urls', action='store_true', default=False,
    help='Download shapefiles by ISO')

group.add_argument('--download-by-adm', dest='adm_urls', action='store_true', default=False,
    help='Download shapefiles by admin level')