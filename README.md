python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cloc apartment_manager/apartment_manager.py

python3 main.py

python -m unittest discover

coverage run -m unittest discover

coverage html  

mutmut run
