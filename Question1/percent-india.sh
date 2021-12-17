echo "Running percent-india.sh"

cd ..

if [ ! -d "./env" ]
then
  python3 -m venv env
  source ./env/bin/activate
  pip install -r requirements.txt
  clear
  echo "Running percent-india.sh"
fi


source ./env/bin/activate
python3 ./Question1/p1.py
