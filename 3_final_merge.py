import re
import pandas as pd

# load fiscrep
fiscrep = pd.read_pickle('merged_fiscrep.pickle')



# load CFR_data european
CFR_data = pd.read_pickle('CFR_data_cut.pickle')

# Remove duplicates
CFR_data.drop_duplicates(subset='CFR', keep='last', inplace=True)

# A list of variables to select
CFR_data = CFR_data[['CFR',
                    #'Event', 
                    #'Event Start Date', 
                    #'Event End Date', 
                    'Registration Number', 
                    #'External marking', 
                    #'Name of vessel', 
                    'Place of registration', 
                    #'IRCS', 
                    #'IRCS indicator', 
                    #'Licence indicator', 
                    #'VMS indicator', 
                    #'ERS indicator', 
                    #'AIS indicator', 
                    #'MMSI', 
                    'Vessel Type', 
                    'Main fishing gear', 
                    'LOA', 
                    #'LBP', 
                    #'Tonnage GT', 
                    #'Other tonnage', 
                    #'GTs', 
                    #'Power of main engine', 
                    #'Power of auxiliary engine', 
                    #'Hull material', 
                    #'Country_imp_exp', 
                    'Year of construction', 
                    'Active']]

# Rename to merge in CFR_data
CFR_data.rename(columns = {'CFR': 'matched_CFR'},inplace=True)

# Use merge to join the two DataFrames on the 'CFR' column
merged_df = fiscrep.merge(CFR_data, on='matched_CFR', how='left')

# Some variable change to make it internationally recognized
variable_change = {'Nº':'Number', 'Nome': 'Name', 'Registration Number_x': 'Reg_Num', 'Unidade':'Unity',
                    'Tip Emb':'Vessel_Type_x', 'Sub Tip': 'Sub_Type', 'Arte':'gear',
                    'Vessel Type':'Vessel_Type_y', 'Main fishing gear':'Gear',
}
merged_df.rename(columns = variable_change, inplace=True)


# check if all checkout (only one is not checked - CFR            PRT000019926     matched_CFR    PRT000007009)
for index, fiscalization in merged_df.iterrows():
    if fiscalization.CFR != 'DESCONHECIDO':
        if fiscalization.CFR != fiscalization.matched_CFR:
            if fiscalization.matched_CFR.startswith('No_CFR'):
                print(fiscalization[['CFR','matched_CFR']])

merged_df['local'] = 'Foreign'

for index, fiscalization in merged_df.iterrows():
    if isinstance(fiscalization.Reg_Num,str):
        reg = fiscalization.Reg_Num.split('-')
        if len(reg) == 3:
            merged_df.local.iloc[index] = reg[0]
        else:
            print(fiscalization.Reg_Num)

loc_to_loc = pd.read_pickle('loc_to_loc_pair.pickle')

local_convert = pd.DataFrame({'old': [], 'new': []})

for index, local in loc_to_loc.iterrows():
    if local.Last_License.startswith('PT'):
        if not local.Previous_License.startswith('PT'):
            local_convert = local_convert.append({'old': local.Previous_License, 'new': local.Last_License}, ignore_index=True)

print(local_convert)

merged_df['real_local'] = merged_df['local'].where(
    merged_df['local'].isin(['Foreign', 'PT']), 
    merged_df['local'].map(local_convert.set_index('old')['new'])
).fillna(merged_df['local'])



local_description = pd.read_csv('table_locais.csv')[['LOCODE_T','NameWoDiacritics']]

merged_df = merged_df.merge(local_description, left_on='real_local', right_on='LOCODE_T', how='left')

merged_df = merged_df.drop(columns='LOCODE_T')





# create an empty dataframe to store the results
results_df = pd.DataFrame(columns=['Real Local', 'Names', 'Count'])

# iterate over the unique real locals
for loc in merged_df.real_local.unique():
    # get the names for the current real local
    names = merged_df.loc[merged_df.real_local == loc, "NameWoDiacritics"]
    # count the number of results
    count = len(names)
    # create a new row with the real local, names, and count

    row = {'Real Local': loc, 'Names': names.unique()[0], 'Count': count}
    # add the row to the results dataframe
    results_df = results_df.append(row, ignore_index=True)

# save the results to an Excel file
results_df.to_excel('results.xlsx', index=False)




# Some more cleaning to do 'TODOS ' transformed to LEGAL
merged_df['Result'] = merged_df['Result'].replace('TODOS ', 'LEGAL ')



# apply strip function to all string values in the DataFrame to remove space in the end
merged_df = merged_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)



#Separate the infractions by commas and save it in arrays
merged_df["Infrac_a"] = merged_df.Infrac.apply(lambda x: x.split())



# Create a set to hold all unique infractions in the DataFrame
all_infractions = set()

# Iterate over the Infrac column to get all unique infractions
for infrac_list in merged_df.Infrac_a:
    all_infractions.update(infrac_list)

# Define a dictionary that maps each infraction to its numeric value
infraction_values = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                     'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
                     'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14}

# Sort the keys of the dictionary based on their values
sorted_infractions = sorted(infraction_values, key=infraction_values.get)

# Create indicator columns for each infraction in the sorted order
for infraction in sorted_infractions:
    merged_df[infraction] = merged_df.Infrac_a.apply(lambda x: infraction in x).astype(int)


merged_df['number_infracs'] = [len(infrac_a) for infrac_a in merged_df.Infrac_a]
merged_df['Year'] = [data.year for data in merged_df.GDH]


# print the modified DataFrame
print(merged_df.head())


nuts_codes = pd.read_excel(r'para_nuts_complete.xlsx')

NutsII_Code = []

for i, vessel in merged_df.iterrows():
    local = merged_df.NameWoDiacritics[i]
    if local == local:
        code = nuts_codes[nuts_codes.Local == local].Code.values[0]
        print(code)
        NutsII_Code.append(code)
    else:
        NutsII_Code.append(local)

merged_df['NUTSII_code'] = NutsII_Code



import pandas as pd 
import numpy as np
from conversion_coordinates import dms_to_dd

df = pd.read_pickle('final_fiscrep.pickle')


def dms_to_dd(dms):
    if not dms:  # handle empty or None input
        return None
    degrees, minutes, seconds = 0, 0, 0
    parts = dms.replace('´', '\'').split('º')  # replace `´` with `'`
    if len(parts) > 1:
        degrees = int(parts[0])
        subparts = parts[1].split('\'')
        if len(subparts) > 1:
            minutes = int(subparts[0])
            seconds = float(subparts[1][:-1])
    decimal_degrees = degrees + minutes/60 + seconds/3600
    if dms.endswith(('S', 'W')):
        decimal_degrees *= -1
    return decimal_degrees

df['lat_DD'] = df['Latitude'].apply(dms_to_dd)
df['lon_DD'] = df['Longitude'].apply(dms_to_dd)

df.drop(columns=['Latitude','Longitude'], inplace=True)


print(df.head())

merged_df['lat_DD'] = df['lat_DD']
merged_df['lon_DD'] = df['lon_DD']


#select in the column 'NUTSII_code' just the PTXX, and the fiscalizations that were realized in the 2023 year
merged_df = merged_df.dropna(subset=['NUTSII_code'])
merged_df = merged_df.dropna(subset=['Year'])
merged_df = merged_df[~(merged_df['Year'].astype(str) == '2023')]
df = df.dropna(subset=['Year'])
df = df[~(df['Year'].astype(str) == '2023')]




#create a new column with the security (S) and fishery (P)  
import numpy as np

merged_df['security'] = np.nan
merged_df['security'] = merged_df['Infrac_a'].apply(lambda x: 'S' if any(infrac in ['XII', 'XIII', 'XIV'] for infrac in x) else np.nan)

merged_df['fishery'] = np.nan
merged_df['fishery'] = merged_df['Infrac_a'].apply(lambda x: 'P' if any(infrac in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'] for infrac in x) else np.nan)


#remove number to clean the html map, because they are located in land
#numbers_to_remove = [13579, 13580, 13590, 13593, 13594, 13601, 13602, 13606, 13607, 13618, 13619, 13621, 13622, 13628, 13634, 13641, 13643, 13644, 13645, 13651, 13652, 13653, 13655, 13656, 13657, 13660, 13661, 13664, 13665, 13666, 13667, 13668, 13672, 13673, 13674, 13675, 13679, 13680, 13681, 13682, 13684, 13685, 13687, 13689, 13690, 13691, 13693, 13694, 13695, 13696, 13698, 13699, 13705, 13708, 13710, 13711, 13589, 13591, 13603, 13608, 13609, 13612, 13638, 13639, 13640, 13642, 13654, 13659, 13663, 13671, 13683, 13697, 13700, 13703, 13704, 13707, 13678, 13702, 13636, 13583, 13584, 13623, 13635, 13637, 13658, 13676, 13701, 13581]

#df = df[~df['Number'].isin(numbers_to_remove)]
#merged_df = merged_df[~merged_df['Number'].isin(numbers_to_remove)]

#Delete duplicated lines
merged_df = df.drop_duplicates(subset='Number', keep='last')
df = df.drop_duplicates(subset='Number', keep='last')

df = merged_df

# save merged data
merged_df.to_csv('final_fiscrep.csv')
merged_df.to_pickle('final_fiscrep.pickle')
merged_df.to_excel('final_fiscrep.xlsx')



print(merged_df.columns)


#Count the number of Infractions that are considered 'S' and 'P'
#sum_value = merged_df.loc[(merged_df['security'] == 'S') & (merged_df['fishery'] == 'P')].count()

# Display the first few rows of the dataset
print(df.head())

# Generate summary statistics for the numerical variables
print(df.describe())

# Display the column names, data types, and number of non-null values for each variable
print(df.info())

# Count the number of missing values in each column
print(df.isnull().sum())

# Count the number of unique values in each column
#print(df.nunique())











