!/bin/bash
1.4.6

function getRepo {
    sudo apt-get install git
    curl -H "Accept: application/json" -X GET "$base_url/downloadRSA" > ~/home/ubuntu/id_rsa
    eval "$(ssh-agent -s)"
    ssh-add /home/ubuntu/.ssh/id_rsa
    mkdir /home/ubuntu/service
    git clone git@github.com:h3y4w/dissect-services.git ~/service
}
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file

getRepo


