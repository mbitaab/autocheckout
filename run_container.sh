#!/bin/bash

# /mnt/marzi/experminets/scam_collector/scam_directory/crawled/scam_dir_2024-03-29.txt

docker run -d \
    -v /mnt/marzi/experminets/scam_collector/buster/crawled:/input \
    -v /mnt/marzi/experminets/scam_collector/buster/ac_result:/output \
    -v /mnt/marzi/experminets/scam_collector/logs:/logs/ \
    -v /mnt/marzi/experminets/scam_collector/checkout_pages:/checkout_pages/ \
    -v /mnt/marzi/experminets/scam_collector/screenshots:/screenshots/ \
    --network="host"  \
    ac \
    python ./src/app.py \
    --input_bp /input/scam_dir_2024-03-29.txt \
    --p_log_file_address /output/scam_dir_2024-03-29.jsonl \
    --log_file_address /logs/scam_dir_2024-03-29.log \
    --html_file_address /checkout_pages/ \
    --screen_file_address /screenshots/ \

