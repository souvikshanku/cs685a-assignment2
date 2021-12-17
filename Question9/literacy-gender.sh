echo "Running literacy-gender.sh"
cd ..

if [ ! -d "./env" ]
then
  python3 -m venv env
  source ./env/bin/activate
  pip install -r requirements.txt
  clear
  echo "Running literacy-gender.sh"
fi



source ./env/bin/activate
python3 ./Question9/p9.py
