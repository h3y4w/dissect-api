#!/bin/bash
#0.0.1

export api_ip=%s
export api_url='http://%s'
export manager_type='%s'
base_url=$(printenv api_ip)

function downloadSource {
    cd /home/ubuntu
    wget https://github.com/h3y4w/dissect-worker/archive/master.zip
    unzip master.zip worker
}

function downloadWorkerScript {
    cd /home/ubuntu/
    curl -H "Accept: application/json" -X GET "$base_url/worker/download/run" > run_worker.sh
}
function run {
    cd /home/ubuntu/worker
    python main.py 
}

downloadSource
downloadWorkerScript
run
