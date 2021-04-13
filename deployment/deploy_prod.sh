#!/bin/sh

ssh ubuntu@10.0.2.15 <<EOF
  cd fedupjobs
  git pull
  source /opt/envs/fedupjobs/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  sudo supervisorctl restart fedupjobs
  exit
EOF