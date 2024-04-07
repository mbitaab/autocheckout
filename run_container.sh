#!/bin/bash

docker run -d \
    -v /mnt/ssd2/test:/app/data \
    --network="host"  \
    ac \
    python ./src/app.py \
    --input_bp "/app/data/domain.csv" \
    --p_log_file_address /app/data/test_2024-03-07.jsonl \
    --log_file_address /app/data/test_2024-03-07.log \
    --html_file_address /app/data/ \
    --screen_file_address /app/data/
