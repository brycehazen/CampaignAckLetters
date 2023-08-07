Purpose
The purpose of this script is to process and merge specific CSV files in a directory. The script identifies a file with "Export" in its name, cleans it, and then merges it with another CSV file based on specific columns.

Requirements
Python 3.x
pandas library (can be installed via pip install pandas)
How to run
Place the script in a directory containing the CSV files you want to process. Ensure one file has "Export" in its name and the other contains the column "Constituent ID". Then, execute the script:

Copy code
python script_name.py
Replace script_name.py with the name you've saved the script as.

Input and Output
Input:

A CSV file with "Export" in its name which will undergo cleaning.
Another CSV file containing a column "Constituent ID" for merging.
Output:

A cleaned version of the "Export" file with "_clean" appended to its name.
A merged file of the cleaned "Export" file and the other CSV, saved with "_merged" appended to the original "Export" file's name.
Description
The script performs the following steps:

Identifies and reads the CSV file with "Export" in its name.
Cleans the "Export" file. (Note: Ensure you integrate the relevant cleaning steps where indicated in the script.)
Identifies another CSV file in the directory which contains the column "Constituent ID".
Merges the cleaned "Export" file with this second file.
Renames columns to more user-friendly names.
Saves the merged data with "_merged" appended to the original "Export" file's name.
