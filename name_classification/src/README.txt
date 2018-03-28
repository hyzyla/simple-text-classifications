Gender Predictor is in gender_predictor.py 
This one file that you need. 
This file uses only one dependency numpy.
For installing numpy type in console: pip install numpy 
For using predictor just import from gender_predictor.py needed a function or a class.
Before using you need load data for prediction. There are two options:
1) load from a file with names or use 'pickled' object. After loading from file you can 'pickle' object and in the future use second faster option
2) load from 'pickled' object. It's faster than loading from file. (Be attempted: You need to have text files with female and male names separately)
Please, see to the test.py for better understanding how to use it.


Also, small command line script for predict names from xlsx or csv (need openpyxl module: for install it: pip install openpyxl). Examples:
1) python predict2xlsx.py file_for_opening.xlsx --sheet "Sheet 1" --name-column A --offset 20 --gender-column C
This script reads file_for_opening.xlsx, opens "Sheet 1", reads column A from 20 row and writes predicted gender to column C
2)python predict2xlsx.py all_37k_names.csv --write-path result.csv
This script reads all_37k_names.csv, writes name and predicted gender to file result.csv

