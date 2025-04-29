#!/bin/bash
cd /app

case "$1" in
  extract)
    cd monitores_etl/extraction
    exec scrapy crawl monitor -o ../../data/raw_data.json
    ;;
  transform)
    exec python3 -m monitores_etl.transformLoad.main
    ;;
  dashboard)
    exec streamlit run monitores_etl/dashboard/app.py
    ;;
  *)
    echo "Uso: docker run <container> {extract|transform|dashboard}"
    exit 1
    ;;
esac

