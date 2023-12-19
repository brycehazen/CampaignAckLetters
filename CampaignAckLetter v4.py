import glob
import pandas as pd
import numpy as np
import os

# Find the file with "Export" in its name
export_files = [f for f in glob.glob('*.*') if "Export" in f]
if not export_files:
    raise ValueError("No file with 'Export' in its name found.")
export_file = export_files[0]

# Read the 'Export' file and clean it
df = pd.read_csv(export_file,low_memory=False,encoding='ISO-8859-1')


# Any file ending in csv
files = glob.glob('*.CSV')

# List of all RE titles
AllREtitles = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                 'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                 'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.', 'Family of']

# List of  special  titles
specialTitle = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                 'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                 'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Family of']

# List of common titles
commonTitles = ['Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.','Sra.', 'Señor']                

# # Loop through all files in directory
# for file in files:
#     df = pd.read_csv(file, encoding='latin-1', low_memory=False)
#     # Replaces all spaces with nan
#     df = df.replace([''], np.nan)

#     # drops row if address is blank
#     # df = df.dropna(subset=['CnAdrPrf_Addrline1'])
#     # drop row if all name information are blank - estates and orgs
#     # df = df.dropna(subset=['Gf_CnBio_First_Name', 'Gf_CnBio_Last_Name', 'Gf_CnSpSpBio_First_Name', 'Gf_CnSpSpBio_Last_Name'], how='all')
#     # drops duplicate ConsID
#     df = df.drop_duplicates(subset=['Gf_CnBio_ID'])

# Define a function to remove data based on conditions
def remove_data_based_on_conditions(row):
    # Check if 'Gf_CnBio_First_Name' is equal to 'Gf_CnSpSpBio_First_Name' and remove data if True
    if row['Gf_CnBio_First_Name'] == row['Gf_CnSpSpBio_First_Name']:
        row['Gf_CnSpSpBio_Gender'] = ''
        row['Gf_CnSpSpBio_Title_1'] = ''
        row['Gf_CnSpSpBio_First_Name'] = ''
        row['Gf_CnSpSpBio_Last_Name'] = ''

    # Check if 'Gf_CnSpSpBio_Inactive' or 'Gf_CnSpSpBio_Deceased' is 'Yes' and remove data if True
    if row['Gf_CnSpSpBio_Inactive'] == 'Yes' or row['Gf_CnSpSpBio_Deceased'] == 'Yes' or ['Gf_CnBio_Marital_status'] == 'Widowed' or ['Gf_CnBio_Marital_status'] == 'Divorced':
        row['Gf_CnSpSpBio_Gender'] = ''
        row['Gf_CnSpSpBio_Title_1'] = ''
        row['Gf_CnSpSpBio_First_Name'] = ''
        row['Gf_CnSpSpBio_Last_Name'] = ''

    return row

# Apply the function to your DataFrame
df = df.apply(remove_data_based_on_conditions, axis=1)

def swap_rows_based_on_gender(row):
    if row['Gf_CnBio_Gender'] == 'Female' and row['Gf_CnSpSpBio_Gender'] == 'Male':
        temp_gender = row['Gf_CnBio_Gender']
        temp_first_name = row['Gf_CnBio_First_Name']
        temp_last_name = row['Gf_CnBio_Last_Name']
        temp_title = row['Gf_CnBio_Title_1']

        row['Gf_CnBio_Gender'] = row['Gf_CnSpSpBio_Gender']
        row['Gf_CnBio_First_Name'] = row['Gf_CnSpSpBio_First_Name']
        row['Gf_CnBio_Last_Name'] = row['Gf_CnSpSpBio_Last_Name']
        row['Gf_CnBio_Title_1'] = row['Gf_CnSpSpBio_Title_1']

        row['Gf_CnSpSpBio_Gender'] = temp_gender
        row['Gf_CnSpSpBio_First_Name'] = temp_first_name
        row['Gf_CnSpSpBio_Last_Name'] = temp_last_name
        row['Gf_CnSpSpBio_Title_1'] = temp_title
    return row

df = df.apply(swap_rows_based_on_gender, axis=1)

# Removes row if they have a solicit code 
def filter_and_remove_solicitations():
    # Get all .csv and .CSV files in the current directory with 'Export' or 'export' in the name
    csv_files = [f for f in os.listdir() if (f.lower().endswith('.csv') and ('Export' in f or 'export' in f))]

    # If no matching files found, return a message
    if not csv_files:
        return "No matching .csv or .CSV files found."

    for file in csv_files:
        df = pd.read_csv(file)

        # List of columns to check
        columns_to_check = [f'CnSolCd_1_{i:02d}_Solicit_Code' for i in range(1, 9)]

        # List of strings to search for  'No OCA Solicitations','No OCA reminders', 'No campaign Reminders'
        strings_to_search = [
            'no mail', 'Requested Removal', 
            'Do not Solicit', 'Do not mail or email'
        ]

        # Create a boolean mask for rows to keep
        mask = df[columns_to_check].isin(strings_to_search).any(axis=1)

        # Save removed rows to CSV
        removed_file_path = os.path.splitext(file)[0] + "_Removed_SolicitCodes.csv"
        removed_df = df[mask]
        removed_df.to_csv(removed_file_path, index=False)

        # Filter the original DataFrame to keep only the desired rows
        df = df[~mask]
        
        # Overwrite the original file with the filtered data
        df.to_csv(file, index=False)

    return "Processing complete for matching files."

# This function update Ms and Miss to mrs if the last names are the same and marital status is married 2016-8067
def update_titles_if_married(row):
    if (row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] == 'Married' or row['Gf_CnSpSpBio_Marital_status'] == 'Married') and (row['Gf_CnBio_Title_1'] != 'Mr.') and (row['Gf_CnSpSpBio_Title_1'] == 'Miss' 
        or row['Gf_CnSpSpBio_Title_1'] == 'Ms.' or row['Gf_CnBio_Title_1'] == 'Miss' or row['Gf_CnBio_Title_1'] == 'Ms.'):
        row['Gf_CnSpSpBio_Title_1'] = 'Mrs.'
        row['Gf_CnBio_Title_1'] = 'Mrs.'
    return row
df = df.apply(update_titles_if_married, axis=1)

# This function update blanks titles to mr if gender is male or sptitle is mrs, ms, or miss
def update_titles_if_blank_mr(row):
    if (pd.isnull(row['Gf_CnBio_Title_1']) and pd.notnull(row['Gf_CnBio_Last_Name']) and (row['Gf_CnBio_Gender'] == 'Male' or row['Gf_CnSpSpBio_Title_1'] == 'Mrs.' or row['Gf_CnSpSpBio_Title_1'] == 'Ms.' or row['Gf_CnSpSpBio_Title_1'] == 'Miss')):
        row['Gf_CnBio_Title_1'] = 'Mr.'
    return row
df = df.apply(update_titles_if_blank_mr, axis=1)

# This function updates blank titles to ms if gender is female or sptitle Mr.
def update_titles_if_blank_ms(row):
    if (pd.isnull(row['Gf_CnBio_Title_1']) and pd.notnull(row['Gf_CnBio_Last_Name']) and (row['Gf_CnBio_Gender'] == 'Female' or row['Gf_CnSpSpBio_Title_1'] == 'Mr.')):
        row['Gf_CnBio_Title_1'] = 'Ms.'
    return row
df = df.apply(update_titles_if_blank_ms, axis=1)

# This function updates blank sptitles to mr if gender is male or title is mrs, ms, or miss
def update_sptitles_if_blank_mr(row):
    if (pd.isnull(row['Gf_CnSpSpBio_Title_1']) and pd.notnull(row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnSpSpBio_Gender'] == 'Male' or row['Gf_CnBio_Title_1'] == 'Mrs.' or row['Gf_CnBio_Title_1'] == 'Ms.' or row['Gf_CnBio_Title_1'] == 'Miss')):
        row['Gf_CnSpSpBio_Title_1'] = 'Mr.'
    return row
df = df.apply(update_sptitles_if_blank_mr, axis=1)

# This function updates blanks sptitles to ms if gender is female or title is mr
def update_sptitles_if_blank_ms(row):
    if (pd.isnull(row['Gf_CnSpSpBio_Title_1']) and pd.notnull(row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnSpSpBio_Gender'] == 'Female' or row['Gf_CnBio_Title_1'] == 'Mr.')):
        row['Gf_CnSpSpBio_Title_1'] = 'Ms.'
    return row
df = df.apply(update_sptitles_if_blank_ms, axis=1)

#If marital status is blank and Last names are  equal, fill in with married. They might be brother and sister, but Add/sal will be mostly the same. 
def update_marital_status_if_blank_married(row):
    if (((pd.isnull(row['Gf_CnBio_Marital_status']) or (row['Gf_CnBio_Marital_status'] == 'Single')) and (row['Gf_CnSpSpBio_Last_Name'] == row['Gf_CnBio_Last_Name'])) or ((row['Gf_CnSpSpBio_Last_Name'] != row['Gf_CnBio_Last_Name']) and pd.notnull(row['Gf_CnSpSpBio_Last_Name']) )):
        row['Gf_CnBio_Marital_status'] = 'Married'
    return row
df = df.apply(update_marital_status_if_blank_married, axis=1)

def update_marital_status_Widowed(row):
    # Check if spouse-related fields are all blank
    spouse_info_blank = all(pd.isnull(row[field] ) or row[field].strip() == '' for field in ['CnSpSpBio_Title_1', 'CnSpSpBio_First_Name', 'CnSpSpBio_Last_Name'])

    # Update marital status to 'Widowed' based on specified conditions
    if ((row['CnSpSpBio_Deceased'] == 'Yes') or 
        (row['CnSpSpBio_Inactive'] == 'Yes') or 
        (row['CnBio_Marital_status'] == 'Divorced') or 
        ((row['CnBio_Marital_status'] in ['Single', 'Married', 'Unknown', None] or pd.isnull(row['CnBio_Marital_status'])) and spouse_info_blank)):
        row['CnBio_Marital_status'] = 'Widowed'
    return row

# Apply the function to the DataFrame
df = df.apply(update_marital_status_Widowed, axis=1)

# If last names are different
def Different_Last_Name_1(row):
    # Check if last names are different, marital status is 'Married', 
    # and either first name or last name of the spouse is not null/blank
    if (row['CnBio_Last_Name'] != row['CnSpSpBio_Last_Name']) and \
    (row['CnBio_Marital_status'] == 'Married') and \
    ((pd.notnull(row['CnSpSpBio_First_Name']) and row['CnSpSpBio_First_Name'].strip()) or \
    (pd.notnull(row['CnSpSpBio_Last_Name']) and row['CnSpSpBio_Last_Name'].strip())):
        row['CnBio_Marital_status'] = 'DifferentLastName_1'
    return row

# Apply the function to the DataFrame
df = df.apply(Different_Last_Name_1, axis=1)

# If last names are different but titles are the same and neither are special
def Same_Last_Name_Same_Title_NonSpecial_2(row):
    global specialTitle # uses list of titles, global is used so that it can be accessed inside the functions
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Title_1'] == row['Gf_CnSpSpBio_Title_1']) and (row['Gf_CnBio_Marital_status'] == 'Married') and (row['Gf_CnBio_Title_1'] not in specialTitle) ): # 
            row['Gf_CnBio_Marital_status'] = 'SameLastNameSameTitleNonSpecial_2'
    return row
df = df.apply(Same_Last_Name_Same_Title_NonSpecial_2, axis=1)

# If Last names are the same and the title is the same 
def Same_Last_Name_Same_Title_Special_3(row):
    global specialTitle
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] == 'Married') and (row['Gf_CnBio_Title_1'] == row['Gf_CnSpSpBio_Title_1']) and (row['Gf_CnBio_Title_1'] in specialTitle) ):
        row['Gf_CnBio_Marital_status'] = 'SameLastNameSameTitleSpecial_3'
    return row
df = df.apply(Same_Last_Name_Same_Title_Special_3, axis=1)

# If Last names are the same and both have a special title
def Same_Last_Name_Both_Specical_Title_4(row):
    global specialTitle
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] == 'Married') and (row['Gf_CnBio_Title_1'] in specialTitle and row['Gf_CnSpSpBio_Title_1'] in specialTitle) ):
        row['Gf_CnBio_Marital_status'] = 'SameLastNameBothSpecicalTitle_4'
    return row
df = df.apply(Same_Last_Name_Both_Specical_Title_4, axis=1)

# If Last names are the same only main has special title
def Same_Last_Name_Main_Specical_Title_5(row):
    global specialTitle
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] == 'Married') and (row['Gf_CnBio_Title_1'] in specialTitle) ):
        row['Gf_CnBio_Marital_status'] = 'SameLastNameMainSpecicalTitle_5'
    return row
df = df.apply(Same_Last_Name_Main_Specical_Title_5, axis=1) 

# If Last names are the same only spouse has special title
def Same_Last_Name_Sp_Specical_Title_6(row): 
    global specialTitle
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] == 'Married') and (row['Gf_CnSpSpBio_Title_1'] in specialTitle) ):
        row['Gf_CnBio_Marital_status'] = 'SameLastNameSpSpecicalTitle_6'
    return row
df = df.apply(Same_Last_Name_Sp_Specical_Title_6, axis=1)

# Standard Add/sal for married couple
def Standard_Add_Sal_7(row): 
    global commonTitles
    if ((row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']) and (row['Gf_CnBio_Marital_status'] != 'Widowed') and 
        (row['Gf_CnBio_Marital_status'] == 'Married') and ((row['Gf_CnBio_Title_1'] in commonTitles) or (row['Gf_CnSpSpBio_Title_1'] in commonTitles)  ) ):
        row['Gf_CnBio_Marital_status'] = 'StandardAddSal_7'
    return row
df = df.apply(Standard_Add_Sal_7, axis=1) 

def Standard_Add_Sal_MaleSp_8(row):
    global commonTitles
    if (row['Gf_CnBio_Last_Name'] == row['Gf_CnSpSpBio_Last_Name']
        and row['Gf_CnBio_Marital_status'] != 'Widowed'
        and row['Gf_CnBio_Marital_status'] == 'Married'
        and (row['Gf_CnBio_Title_1'] in commonTitles or row['Gf_CnSpSpBio_Title_1'] in commonTitles)
        and row['Gf_CnSpSpBio_Gender'] == 'Male'
    ):
        row['Gf_CnBio_Marital_status'] = 'StandardAddSal_MaleSp_8'
    return row

df = df.apply(Standard_Add_Sal_MaleSp_8, axis=1)

# Name info is blank, cannot concatenate a addsal
def blank_names_Unchanged_AddSal(row):
    if (pd.isnull(row['CnBio_Last_Name']) and pd.isnull(row['CnBio_First_Name'])):
        row['CnBio_Marital_status'] = 'Unchanged'
    return row
df = df.apply(blank_names_Unchanged_AddSal, axis=1)

# fills First and last name with a blank space otherwise it would fill cell with 'nan'
df['Gf_CnBio_First_Name'] = df['Gf_CnBio_First_Name'].loc[:].fillna('')
df['Gf_CnBio_Last_Name'] = df['Gf_CnBio_Last_Name'].loc[:].fillna('')

# Add/sal  
 def concate_add_sal(row):
        # Unchanged
        # Not enough data to concatenate a add/sal
        if (row['CnBio_Marital_status'] == 'Unchanged' ):
            addressee = str(row['CnAdrSal_Addressee'])
            salutation = str(row['CnAdrSal_Salutation'])

        # WidSinDiv_0
        # Mr. Bryce Howard 
        # Mr. Howard
        elif (row['CnBio_Marital_status'] == 'WidSinDiv_0'):
            # Check if Last Name is not blank
            if pd.notnull(row['CnBio_Last_Name']) and row['CnBio_Last_Name'].strip():
                addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name'])
                salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name'])
            # If Last Name is blank, use First Name
            elif pd.notnull(row['CnBio_First_Name']) and row['CnBio_First_Name'].strip():
                addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name'])
                salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name'])
    
    # Different_Last_Name_1
    # Mr. Bryce Howard and Mrs. Jennifer Ha 
    # Mr. Howard and Mrs. Ha
    elif (row['Gf_CnBio_Marital_status'] == 'DifferentLastName_1'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name']) +' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' +  str( row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])

    # Same_Last_Name_Same_Title_NonSpecial_2
    # Mr. Bryce Howard and Mr. Branden Howard
    # Mr Howard and Mr. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'SameLastNameSameTitleNonSpecial_2'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name']) +' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' +  str( row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name'])

    # Gives: Same_Last_Name_Same_Title_Special_3
    # Dr. Bryce Howard and Dr. Jen Howard
    # Dr. Howard and Dr. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'SameLastNameSameTitleSpecial_3'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' +  str( row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])

    # Same_Last_Name_Both_Specical_Title_4 
    # Senator Bryce Howard and Dr. Jen Howard
    # Senator Howard and Dr. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'SameLastNameBothSpecicalTitle_4'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' +  str( row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])

    # Same_Last_Name_Main_Specical_Title_5 
    # Dr. Bryce Howard and Mrs. Howard
    # Dr. Howard and Mrs. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'SameLastNameMainSpecicalTitle_5'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' +  str( row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])       
    
    # Same_Last_Name_Sp_Specical_Title_6 
    # Dr. Jennifer Howard and Mr. Bryce Howard
    # Dr. Howard and Mr. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'SameLastNameSpSpecicalTitle_6'):
        addressee = str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name']) + ' and ' + str(row['Gf_CnBio_Title_1']) + ' ' +  str( row['Gf_CnBio_Last_Name'])
        salutation = str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name']) + ' and ' + str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name'])      
    
    # Standard_Add_Sal_7
    # Mr. and Mrs. Bryce Howard
    # Mr. and Mrs. Howard
    elif (row['Gf_CnBio_Marital_status'] == 'StandardAddSal_7'):
        addressee = str(row['Gf_CnBio_Title_1']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnBio_First_Name']) + ' ' + str(row['Gf_CnBio_Last_Name'])
        salutation = str(row['Gf_CnBio_Title_1']) + ' and ' + str(row['Gf_CnSpSpBio_Title_1']) + ' ' + str(row['Gf_CnBio_Last_Name'])

    elif (row['Gf_CnBio_Marital_status'] == 'Standard_Add_Sal_MaleSp_8'):
        addressee = str(row['Gf_CnSpSpBio_Title_1']) + ' and ' + str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_First_Name']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])
        salutation = str(row['Gf_CnSpSpBio_Title_1']) + ' and ' + str(row['Gf_CnBio_Title_1']) + ' ' + str(row['Gf_CnSpSpBio_Last_Name'])

    # This will make the add/sal blank, which will help find edge cases. Any add/sal that did not fit the criteria above, will come out blank.   
    else:
        addressee = ''
        salutation = ''
    return pd.Series({'CnAdrSal_Addressee': addressee, 'CnAdrSal_Salutation': salutation})

# applies the function to the Add/sal field
df[['CnAdrSal_Addressee', 'CnAdrSal_Salutation']] = df.apply(concate_add_sal, axis=1)


# list of columns_to_drop I stopped droppping columns and decided to do that manually after this runs to better trouble shoot any issues.
#columns_to_drop = ['CnAdrPrf_Type', 'CnAdrPrf_Sndmailtthisaddrss', 'Gf_CnSpSpBio_Anonymous', 'Gf_CnBio_Gender', 'Gf_CnSpSpBio_Gender', 
                    #'Gf_CnSpSpBio_Inactive', 'Gf_CnSpSpBio_Deceased',   'Gf_CnSpSpBio_Marital_status', 'Gf_CnBio_Marital_status']

#'Gf_CnBio_Inactive','Gf_CnSpSpBio_ID', 'Gf_CnBio_Deceased', 'Gf_CnBio_Anonymous', 'Gf_CnBio_Title_1', 'Gf_CnSpSpBio_Title_1', 'Gf_CnSpSpBio_First_Name', 'Gf_CnSpSpBio_Last_Name','Gf_CnBio_Org_Name',,'Gf_CnBio_Org_ID', 

# drops columns in list
#df = df.drop(columns=columns_to_drop)
# Sort the DataFrame by 'Gf_CnBio_Last_Name' and 'Gf_CnBio_First_Name'


# Save the cleaned file with '_clean' suffix
base, ext = os.path.splitext(export_file)
clean_file = base + '_clean' + ext
df.to_csv(clean_file, index=False, encoding='ISO-8859-1')

# Find the other file in the directory with 'Constituent ID' column
other_files = [f for f in glob.glob('*.*') if f != export_file]
for other_file in other_files:
    try:
        other_df = pd.read_csv(other_file, encoding='ISO-8859-1')
        if 'Constituent ID' in other_df.columns:
            break
    except:
        continue


# Merge the cleaned dataframe with other_df
merged_df = pd.merge(df, other_df, left_on='Gf_CnBio_ID', right_on='Constituent ID', how='left')

# Rename columns to user-friendly names
column_mapping = {
    'Gf_CnBio_ID': 'Constituent ID',
    'Gf_CnBio_Anonymous': 'Is Anonymous?',
    'Gf_CnBio_Title_1': 'Title',
    'Gf_CnBio_Gender': 'Gender',
    'Gf_CnBio_Deceased': 'Is Deceased?',
    'Gf_CnBio_Inactive': 'Is Inactive?',
    'Gf_CnBio_First_Name': 'First Name',
    'Gf_CnBio_Last_Name': 'Last Name',
    'Gf_CnBio_Marital_status': 'Marital Status',
    'Gf_CnBio_No_Valid_Addresses': 'No Valid Addresses?',
    'Gf_CnSpSpBio_ID': 'Spouse ID',
    'Gf_CnSpSpBio_Anonymous': 'Spouse Is Anonymous?',
    'Gf_CnSpSpBio_Title_1': 'Spouse Title',
    'Gf_CnSpSpBio_Gender': 'Spouse Gender',
    'Gf_CnSpSpBio_Deceased': 'Spouse Deceased?',
    'Gf_CnSpSpBio_Inactive': 'Spouse Inactive?',
    'Gf_CnSpSpBio_First_Name': 'Spouse First Name',
    'Gf_CnSpSpBio_Last_Name': 'Spouse Last Name',
    'Gf_CnSpSpBio_Marital_status': 'Spouse Marital Status',
    'Gf_CnAdrSal_Addressee': 'Addressee',
    'Gf_CnAdrSal_Salutation': 'Salutation',
    'Gf_CnAdrPrf_Addrline1': 'Address Line 1',
    'Gf_CnAdrPrf_Addrline2': 'Address Line 2',
    'Gf_CnAdrPrf_City': 'City',
    'Gf_CnAdrPrf_State': 'State',
    'Gf_CnAdrPrf_ZIP': 'ZIP Code'
    # ... add more columns as needed
}

merged_df = merged_df.rename(columns=column_mapping)
# Save the merged dataframe with a '_merged' suffix
merged_file = base + '_merged' + ext
merged_df.to_csv(merged_file, index=False, encoding='ISO-8859-1')
