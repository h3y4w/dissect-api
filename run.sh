!/bin/bash
1.4.6

function runRepo {
    cd /home/ubuntu
    python dissect-workers/test.py
}
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file

runRepo



