!/bin/bash
1.4.6

function getandRunRepo {
    curl -H "Accept: application/json" -X GET "$base_url/downloadRSA" > /home/ubuntu/.ssh/id_rsa
    eval "$(ssh-agent -s)"
    sudo ssh-add /home/ubuntu/.ssh/id_rsa
    cd /home/ubuntu/
    sudo git clone git@github.com:h3y4w/dissect-workers.git
    cd dissect-workers
    python test.py
}
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file

getandRunRepo



