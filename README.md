# CSV Processing and Merging Script

This script processes and merges specific CSV files within a directory. It's designed to identify a file with "Export" in its  name, perform cleaning operations on it, and then merge it with another CSV file based on specific columns. One file comes from the Mail Module while the file with 'Export' in its name will come from the query created by the Mail module, which you the export from the Export module. 

## Table of Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Detailed Steps](#detailed-steps)

## Requirements
- **Python**: Version 3.x
- **Libraries**: pandas (Install via `pip install pandas`)
- Run Mail module to genderate csv
- Export Query created from Mail module run
- This exported query needs to have Export in the name
- Must clean up Query Export (titles, Genders)

## Usage

1. Ensure your working directory contains the CSV files for processing.
2. One of the files should contain "Export" in its name.
3. Another file in the directory should have the column "Constituent ID".
4. Run the script using the command:
    ```bash
    python CampaignAckLetter.py
    ```
    Replace `CampaignAckLetter.py` with the name you've saved the script as.

## File Descriptions

**Input**:
- `_Export.csv`: A CSV file with "Export" in its name which undergoes cleaning.
- `.csv`: Another CSV file containing the column "Constituent ID" used for merging.

**Output**:
- `_Export_clean.csv`: A cleaned version of the "Export" file.
- `_Export_merged.csv`: A merged file of the cleaned "Export" file and the other CSV.

## Detailed Steps

1. **Identification**: The script finds and reads the CSV file with "Export" in its name.
2. **Cleaning**: Processes the identified "Export" file. (Make sure to integrate the relevant cleaning steps where indicated in the script.)
3. **Merging**: Identifies another CSV file in the directory which contains the "Constituent ID" column. Merges the cleaned "Export" file with this second file.
4. **Renaming**: Updates column names to be more user-friendly.
5. **Saving**: Outputs the merged data with a "_merged" suffix added to the original "Export" file's name.
