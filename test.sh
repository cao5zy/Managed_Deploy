source .env/bin/activate

.env/bin/pylint src/deploy.py --rcfile pylint.rc
nosetests --nologcapture -s tests -w /root/specialist/Managed_Deploy/src
