import pandas as pd
import numpy as np

# load fiscrep data from a pickle file
fiscrep = pd.read_pickle('checked_fiscrep_2.pickle')

# load CFR_data european data from a pickle file
CFR_data = pd.read_pickle('CFR_data_cut.pickle')

# drop duplicate rows based on 'Registration Number' column in CFR_data
CFR_data.drop_duplicates(subset='Registration Number', keep='first', inplace=True)

# rename column 'nº reg' to 'Registration Number' in fiscrep
fiscrep.rename(columns = {'nº reg':'Registration Number'}, inplace=True)

# merge fiscrep and CFR_data based on 'Registration Number' column and using left join
merged_df = fiscrep.merge(CFR_data[['Registration Number', 'CFR']], on='Registration Number', how='left')

# rename 'CFR_y' column to 'real_CFR' and 'CFR_x' column to 'CFR' in merged_df
merged_df = merged_df.rename(columns={'CFR_y': 'real_CFR', 'CFR_x': 'CFR'})

# load CFR_DGRM data from an Excel file
CFR_DGRM = pd.read_excel('Julho2022.xlsx')
CFR_DGRM2 = pd.read_excel('Julho2021.xlsx')

# split 'TXT_CONJ_IDENT' column by space and keep the first element as 'Registration Number'
CFR_DGRM['Registration Number'] = [reg.split(' ')[0] for reg in CFR_DGRM.TXT_CONJ_IDENT]
CFR_DGRM2['Registration Number'] = [reg.split(' ')[0] for reg in CFR_DGRM2['Conjunto Identificação / Identification Set']]

# drop duplicate rows based on 'Registration Number' column in CFR_DGRM
CFR_DGRM.drop_duplicates(subset='Registration Number', keep='first', inplace=True)
CFR_DGRM2.drop_duplicates(subset='Registration Number', keep='first', inplace=True)

# rename column 'NUM_CFR' to 'CFR' in CFR_DGRM
CFR_DGRM.rename(columns={'NUM_CFR':'CFR'},inplace=True)

# merge merged_df and CFR_DGRM based on 'Registration Number' column and using left join
merged_df2 = merged_df.merge(CFR_DGRM[['Registration Number', 'CFR']], on='Registration Number', how='left')
merged_df3 = merged_df2.merge(CFR_DGRM2[['Registration Number', 'CFR']], on='Registration Number', how='left')

# rename 'CFR_y' column to 'real_CFR_2' and 'CFR_x' column to 'CFR' in merged_df2
merged_df2 = merged_df2.rename(columns={'CFR_y': 'real_CFR_2', 'CFR_x': 'CFR'})
merged_df3 = merged_df3.rename(columns={'CFR_y': 'real_CFR_2', 'CFR_x': 'CFR', 'CFR': 'real_CFR_3'})

# create a new column 'matched_CFR' in merged_df2 with NaN values
merged_df3['matched_CFR'] = np.nan
merged_df2['matched_CFR'] = np.nan

# fill NaN values in 'matched_CFR' column with values from 'real_CFR_2' column and then 'real_CFR' column
merged_df2['matched_CFR'] = merged_df2['matched_CFR'].fillna(merged_df2['real_CFR_2'].fillna(merged_df2['real_CFR']))
merged_df3['matched_CFR'] = merged_df3['matched_CFR'].fillna(merged_df3['real_CFR_3'].fillna(merged_df3['real_CFR_2'].fillna(merged_df3['real_CFR'])))

# fill remaining NaN values in 'matched_CFR' column with 'No_CFR' string
merged_df2['matched_CFR'] = merged_df2['matched_CFR'].fillna('No_CFR')
merged_df3['matched_CFR'] = merged_df3['matched_CFR'].fillna('No_CFR')

# final definition of CFR based on manual checking
for i, fisc in merged_df3.iterrows():
    if fisc.True_CFR == 1:
        merged_df3.loc[i,'matched_CFR'] = merged_df3.loc[i,'CFR']

# transform all no-CFR in No_CFR_number
No_CFR_ships = merged_df3[merged_df3.matched_CFR=='No_CFR']
No_CFR_ships = No_CFR_ships[['Nome','Registration Number','CFR']]

No_CFR_ships = No_CFR_ships.groupby('Nome')['Registration Number', 'CFR'].agg({'Registration Number': 'unique', 'CFR': 'unique'}).reset_index()

No_CFR_ships['matched_CFR'] = ['NOCFR_'+str(i) for i in range(len(No_CFR_ships))]

No_CFR_ships.to_csv('No_CFR_ships.csv')

for i, ship in No_CFR_ships.iterrows():
    ship_name = ship.Nome
    ship_CFR_code = ship.matched_CFR
    merged_df3.loc[merged_df3.Nome == ship_name, 'matched_CFR'] = ship_CFR_code


# save merged_df3 as a pickle file that has more filled spots
merged_df3.to_pickle('merged_fiscrep.pickle')
