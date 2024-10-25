
admins = ['ADM0', 'ADM1', 'ADM2', 'ADM3']

rule all:
    input:
        expand(
            f"outdir/ETH_{{admin}}/ETH_{{admin}}.shp",
            admin=admins
        )

rule download_geoboundaries:
    output:
        expand(
            f"outdir/ETH_{{admin}}/ETH_{{admin}}.shp",
            admin=admins
        )
    log:
        err="logs/download_geoboundaries_ETH.log"
    shell:
        "python downloader.py geoboundaries=ETH > {log.err}"