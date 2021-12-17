echo "Running 3-to-2-ratio.sh"
cd ..

if [ ! -d "./env" ]
then
  python3 -m venv env
  source ./env/bin/activate
  pip install -r requirements.txt
  clear
  echo "Running 3-to-2-ratio.sh"
fi


source ./env/bin/activate
python3 ./Question4/p4.py
