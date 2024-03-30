#!/bin/bash

CONTAINER_NAME="ac"

CMD="\
    python ./src/app.py \
        --input_bp /input/buster_2024-03-29.txt \
        --p_log_file_address /output//buster_2024-03-29.jsonl \
        --log_file_address /logs/buster_2024-03-29.log \
        --html_file_address /checkout_pages \
        --screen_file_address /screenshots"


docker run --rm --name ac_container_2 \
    -v /mnt/marzi/experminets/scam_collector/buster/crawled:/input \
    -v /mnt/marzi/experminets/scam_collector/buster/ac_result:/output \
    -v /mnt/marzi/experminets/scam_collector/logs:/logs \
    -v /mnt/marzi/experminets/scam_collector/checkout_pages:/checkout_pages \
    -v /mnt/marzi/experminets/scam_collector/screenshots:/screenshots \
    -v /mnt/marzi/experminets/scam_collector/logs:/logs \
    --network=host \
    --entrypoint /bin/bash ${CONTAINER_NAME} -c "${CMD}"