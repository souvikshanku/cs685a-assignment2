#!/bin/env bash
start=$SECONDS

echo "Program Started!"

echo "Creating python virtual environment..."

python3 -m venv ./env
source ./env/bin/activate

echo "Installing Necessary Libraries..."
pip install -r requirements.txt
echo "Installing Necessary Libraries Finished"
clear


#For Question 1
echo "###### Question 1 ######"
cd ./Question1
source ./percent-india.sh
printf "\n\n"

#For Question 2
echo "###### Question 2 ######"
cd ./Question2
source ./gender-india.sh
printf "\n\n"

#For Question 3
echo "###### Question 3 ######"
cd ./Question3
source ./geography-india.sh
printf "\n\n"

#For Question 4
echo "###### Question 4 ######"
cd ./Question4
source ./3-to-2-ratio.sh
#source ./2-to-1-ratio.sh
printf "\n\n"


#For Question 5
echo "###### Question 5 ######"
cd ./Question5
source ./age-india.sh
printf "\n\n"


#For Question 6
echo "###### Question 6 ######"
cd ./Question6
source ./literacy-india.sh
printf "\n\n"


#For Question 7
echo "###### Question 7 ######"
cd ./Question7
source ./region-india.sh
printf "\n\n"


#For Question 8
echo "###### Question 8 ######"
cd ./Question8
source ./age-gender.sh
printf "\n\n"


#For Question 9
echo "###### Question 9 ######"
cd ./Question9
source ./literacy-gender.sh
printf "\n\n"

echo 'Program ended!'

end=$SECONDS
printf "\n\n"
echo "duration: $((end-start)) seconds."
$SHELL

