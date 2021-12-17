CS685 Assignment 2 ReadMe
##########################

Section - 1
##########################
201433-assign2 folder contains the following files - 

1. Question1 - p1.py
             - percent-india.sh
2. Question2 - p2.py
             - gender-india.sh
3. Question3 - p3.py
             - geography-india.sh
4. Question4 - p4.py
             - 3-to-2-ratio.sh
	         - 2-to-1-ratio.sh
5. Question5 - p5.py
             - age-india.sh
6. Question6 - p6.py
             - literacy-india.sh
7. Question7 - p7.py
             - region-india.sh
8. Question8 - p8.py
             - age-gender.sh
9. Question9 - p9.py
             - litearcy-gender.sh
10. assign2.sh
11. requirements.txt
12. README.txt



Section - 2 
##################### 

To run all the programs - 

1. A constant internet connection is required for running the program files.

2. Please install python 3.8 or higher using - $ sudo apt-get install python3.8

3. It is also required to install pip to download the necessary libraries if it 
is not already installed in the machine, using - $ sudo apt-get install python3-pip.

4. Any program within the folder runs via the python virtual envioronment named 'env' and to create it, it is required to install 
the python3-venv package using - $ sudo apt install python3.8-venv.

5. To run the program from the top, a separate script, assign2.sh is provided. To run assign2.sh, first change directory to the
201433-assign2 directory and then run the command - $ bash assign2.sh. To run some individual program, 
please run the shell script in the folder of the corresponding question. 


Section - 3
##################### 

Dependencies among the programs:
For solving question 4, the output of question 1 has been used, so running question1 beforehand is a requirement if question4 is 
to be run. All the other programs can be run inependently.


Section - 4
##################### 

At the end of execution, the folder named 'outputs' should contain 19 files, named as instructed in the Assignment 2 Questions. 
Successful execution of assign2.sh takes roughly 5 minutes.


Thank you for reading!

@ Author: Souvik Bhattacharyya
@ Email: souvik20@iitk.ac.in






