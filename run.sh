!/bin/bash
1.4.6

function getRepo {
    curl -H "Accept: application/json" -X GET "$base_url/downloadRSA" > /home/ubuntu/.ssh/id_rsa
    eval "$(ssh-agent -s)"
    ssh-add /home/ubuntu/.ssh/id_rsa
    sudo mkdir /home/ubuntu/dissect-services
    git clone git@github.com:h3y4w/dissect-services.git /home/ubuntu/dissect-services/ .
}
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /file
sudo mount /dev/xvdb /file

getRepo


