#!/bin/bash
export worker_script_ver=0.0.1
export manager_ip='%s'
export FILE='%s'
function downloadRepo {
    cd /home/ubuntu
    wget https://github.com/h3y4w/dissect-worker/archive/master.zip
    unzip master.zip worker
}

function runRepo {
    cd /home/ubuntu
    python worker/main.py
}

function mountEBS {
    sudo mkfs -t ext4 /dev/xvdb
    sudo mkdir /file
    sudo mount /dev/xvdb /file
}

mountEBS
downloadRepo
runRepo



