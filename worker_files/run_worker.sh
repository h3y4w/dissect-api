#!/bin/bash
#0.0.1
base_url=%s
export FILE='%s'
function downloadRepo {
    cd /home/ubuntu
    wget https://github.com/h3y4w/dissect-worker/archive/master.zip
    unzip master.zip worker
}

function runRepo {
    cd /home/ubuntu
        #python dissect-workers-master/main.py
}

function mountEBS {
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file
}

mountEBS
downloadRepo
runRepo



