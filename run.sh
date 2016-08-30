!/bin/bash
1.4.6

function runRepo {
    cd /home/ubuntu
    python dissect-workers-master/test.py
}

function mountEBS {
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file
}

mountEBS
installRepo
runRepo



