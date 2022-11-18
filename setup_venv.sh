set -eu
virtualenv --python 3.9 ./venv
source venv/bin/activate
pip install -r requirements.txt
