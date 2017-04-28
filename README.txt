This program requires the following python package to run:
	+ numpy	
	+ networkx
	+ random

The program contains two files:
	+ main.py 			---- main function of the program
	+ rwa_adaptive_v12.py   ---- the algorithm class 

To run the program use the command
	python main.py
then the program will ask you for input a number which will be used as a seed for a random generator.


The program will run through 1000 demand cases on the given Network Graph. the output of the program are
	+ the blocking probability over 1000 case ----- blocking case / 1000
			+ the number of blocking in the wavelength assignment process
			+ the number of blocking in the routing process
	+ the average utilization over 1000 case  ----- sum of utilization of 1000 cases / 1000



