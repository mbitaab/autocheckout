#!/bin/bash

docker run -d \
    -v /home/marzie/my_drive/experiments/test_ac:/app/data \
    --network="host"  \
    ac \
    python ./src/app.py \
    --input_bp "/app/data/merged_merchs_2024-03-28.csv" \
    --p_log_file_address /app/data/test_2024-03-29.jsonl \
    --log_file_address /app/data/test_2024-03-29.log \
    --html_file_address /app/data/ \
    --screen_file_address /app/data/
