#!/bin/bash
base_url=%s

function downloadScript {
    curl -H "Accept: application/json" -X GET "$base_url/manager/download/prepare" > run.sh
}

echo $base_url > public_ip
