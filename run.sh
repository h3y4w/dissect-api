!/bin/bash
1.4.6

function installRepo {
    cd /home/ubuntu/
    eval "$(ssh-agent -s)"
    ssh-add id_rsa
    git clone git@github.com:h3y4w/dissect-workers.get
}

function runRepo {
    cd /home/ubuntu
    python dissect-workers/test.py
}

function mountEBS {
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file
}

mountEBS
installRepo
runRepo



