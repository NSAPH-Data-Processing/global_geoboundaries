rule all:
    input:
        "conf/geoboundaries/"

rule download_geoboundaries:
    output:
        "outdir/{iso}_{adm}/"
    log:
        err="logs/download_geoboundaries_{iso}_{adm}.log"
    shell:
        "python downloader.py > {log.err}"