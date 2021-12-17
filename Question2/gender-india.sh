echo "Running gender-india.sh"
cd ..

if [ ! -d "./env" ]
then
  python3 -m venv env
  source ./env/bin/activate
  pip install -r requirements.txt
  clear
  echo "Running gender-india.sh"
fi



source ./env/bin/activate
python3 ./Question2/p2.py
