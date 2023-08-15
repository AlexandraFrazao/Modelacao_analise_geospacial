import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz # library to calculate string similarity
import collections

# read data from Excel file
fiscrep = pd.read_excel(r'FISCREP 2015-2023.xls', sheet_name='RELATOS')

# clean up registration number column by removing anything after a space (the Name was in the reg in some instances)
for i in range(len(fiscrep)):
    reg = fiscrep['nº reg'].iloc[i]
    if isinstance(reg, str) and " " in reg:
        words = reg.split(" ")
        fiscrep.at[i, 'nº reg'] = words[0]

# clean up Tip Emb by removing spaces after word (there are some empty spaces)

for index in range(len(fiscrep)):
    type_v = fiscrep['Tip Emb'].iloc[index]
    if isinstance(type_v,str):
        fiscrep.at[index, 'Tip Emb'] = type_v.rstrip()

# clean the headers of anyspace after the last letter
fiscrep = fiscrep.rename(columns=lambda x: x.rstrip())


# save the unknown registers and decide later
Unknown = fiscrep[fiscrep['Tip Emb'] == 'Desconhecido' ]

CFR_to_local = pd.read_pickle(r'CFR_to_local.pickle')

pd.to_pickle(Unknown, 'Desconhecidos.pickle')

''''''''''''
fiscrep = fiscrep[fiscrep['Tip Emb'] == 'Pesca comercial' ] # we only are goind to address comercial fishing types
''''''''''''

# Identify ships with new regs and old
fiscrep['New_license'] = 0

for index, fiscalization in fiscrep.iterrows():
    reg = fiscalization['nº reg']
    if isinstance(reg, str):
        if reg.startswith('PT') and reg[2].isupper():
            fiscrep.at[index, 'New_license'] = 1

list(fiscrep)

# function getting the most common string
def most_frequent_string(strings):
    counter = collections.Counter(str(x) for x in strings)
    most_common = counter.most_common()
    if len(most_common) > 0:
        return most_common[0][0]
    else:
        return None

# get unique names and registration numbers from data
nome_unique = fiscrep.Nome.unique()
matricula_unique = fiscrep['nº reg'].unique()

# create a new DataFrame to store unique names and their associated registration numbers
ships = pd.DataFrame(nome_unique, columns=['Nome'])
all_regs = []
num_regs = []
likely_reg = []
for ship in nome_unique:
    regs = fiscrep[fiscrep.Nome==ship]['nº reg']
    most_frequent = most_frequent_string(regs)
    regs = list(regs.unique())
    likely_reg.append(most_frequent)
    all_regs.append(regs)
    num_regs.append(len(regs))
ships['registro'] = all_regs
ships['mais_frequente'] = likely_reg
ships['num_regs'] = num_regs

# ships with 1 reg are ok
ships_1_reg = ships[ships.num_regs==1].Nome

ships_more_reg = ships[ships.num_regs>1]

# start colecting fiscrep that are correct
checked_fiscrep = fiscrep[fiscrep.Nome.isin(ships_1_reg)]

# deal with the others
unchecked_fiscrep = fiscrep[~fiscrep.Nome.isin(ships_1_reg)]

# Some letters are not capital letters and that is a mistake...
unchecked_fiscrep['nº reg'] = unchecked_fiscrep['nº reg'].astype(str).str.upper()

# load Portuguese records from 2022
pt_julho_2022_reg = pd.read_excel('Julho2022.xlsx')

pt_julho_2022_reg['Reg'] = [reg.split(' ')[0] for reg in pt_julho_2022_reg.TXT_CONJ_IDENT]

# if registry is in pt then can be collected
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['nº reg'].isin(pt_julho_2022_reg.Reg)]

# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep['nº reg'].isin(pt_julho_2022_reg.Reg)]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)

# load Portuguese records from 2021
pt_julho_2021_reg = pd.read_excel('Julho2021.xlsx')

pt_julho_2021_reg['Reg'] = [reg.split(' ')[0] for reg in pt_julho_2021_reg['Conjunto Identificação / Identification Set']]

# if registry is in pt then can be collected
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['nº reg'].isin(pt_julho_2021_reg.Reg)]

# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep['nº reg'].isin(pt_julho_2021_reg.Reg)]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)





# load CFR_data_cut

CFR_data_cut = pd.read_pickle('CFR_data_cut.pickle')

# if registry is in european comittee then can be collected
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['nº reg'].isin(CFR_data_cut['Registration Number'])]

# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep['nº reg'].isin(CFR_data_cut['Registration Number'])]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)






# All spanish regs have a 3 in the beggining and all portuguese start with PT (new licenses) create column with alternative reg

reg_alt = unchecked_fiscrep['nº reg'].astype(str) # make all strings
unchecked_fiscrep['alternative_reg'] = [reg if reg.startswith(('PT','3')) else '3'+reg for reg in reg_alt] # add 3 to registry
checked_fiscrep['alternative_reg'] = checked_fiscrep['nº reg'].copy() # have same column in checked_fiscrep for concat

# All spanish regs in European are as 3VI***** and not 3-VI****
unchecked_fiscrep['alternative_reg_2'] = [reg.replace('3-', '3', 1).replace('33', '3', 1) if reg.startswith(('3-', '33')) else reg for reg in unchecked_fiscrep['alternative_reg']]
reg_alt2 = checked_fiscrep['alternative_reg'].astype(str) # make all strings
checked_fiscrep['alternative_reg_2'] = [reg.replace('3-', '3', 1).replace('33', '3', 1) if reg.startswith(('3-', '33')) else reg for reg in reg_alt2] 





# if registry is in european comittee then can be collected
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['alternative_reg'].isin(CFR_data_cut['Registration Number'])]

# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep['alternative_reg'].isin(CFR_data_cut['Registration Number'])]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)



# if registry is in european comittee then can be collected
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['alternative_reg_2'].isin(CFR_data_cut['Registration Number'])]

# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep['alternative_reg_2'].isin(CFR_data_cut['Registration Number'])]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)


for reg in unchecked_fiscrep.alternative_reg:
    print(reg)



''''''''''''''''''''''''''''''''''''''''''''''''

# get unique names and registration numbers from data
nome_unique2 = unchecked_fiscrep.Nome.unique()
matricula_unique2 = unchecked_fiscrep['nº reg'].unique()

# create a new DataFrame to store unique names and their associated registration numbers
ships_2 = pd.DataFrame(nome_unique2, columns=['Nome'])
all_regs2 = []
num_regs2 = []
likely_reg2 = []
for ship in nome_unique2:
    regs = unchecked_fiscrep[fiscrep.Nome==ship]['nº reg']
    regs = pd.Series([reg for reg in regs if reg != 'NAN'])
    most_frequent = most_frequent_string(regs)
    regs = list(regs.unique())
    likely_reg2.append(most_frequent)
    all_regs2.append(regs)
    num_regs2.append(len(regs))
ships_2['registro'] = all_regs2
ships_2['mais_frequente'] = likely_reg2
ships_2['num_regs'] = num_regs2

ships_more_reg = ships_2

ships_more_reg['alternative_reg'] = [reg if reg is None or reg.startswith('3') else '3'+reg for reg in ships_more_reg.mais_frequente]

# calculate similarity in the ships with more than one reg

similarities = []
biggest_similarity = []
smallest_similarity = []
for ships in ships_more_reg.itertuples():
    similarities_row = []
    for i in range(len(ships.registro)):
        if isinstance(ships.registro[i], str):
            for j in range(i + 1, len(ships.registro)):
                if isinstance(ships.registro[j], str):
                    # calculate string similarity between two registration numbers using the ratio method
                    dist = fuzz.ratio(ships.registro[i], ships.registro[j])
                    similarities_row.append(dist)
    similarities.append(similarities_row)
    if similarities_row:
        biggest_similarity.append(max(similarities_row))
        smallest_similarity.append(min(similarities_row))
    else:
        biggest_similarity.append(100) # set max similarity to 100 if no registration numbers are found
        smallest_similarity.append(100) # set min similarity to 100 if no registration numbers are found

# add similarity columns to ships DataFrame
ships_more_reg['similarities'] = similarities
ships_more_reg['max_s'] = biggest_similarity
ships_more_reg['min_s'] = smallest_similarity



# Now some ships that had more than one register has only one so 

ships_more_reg_now_1 = ships_more_reg[ships_more_reg.num_regs==1].Nome

# start colecting fiscrep that are correct
unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep.Nome.isin(ships_more_reg_now_1)]


# update unchecked_fiscrep
unchecked_fiscrep = unchecked_fiscrep[~unchecked_fiscrep.Nome.isin(ships_more_reg_now_1)]

# concat results
checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)








# some more checks
for index, fiscalization in checked_fiscrep.iterrows():
    if isinstance(fiscalization['nº reg'], str):
        if fiscalization['nº reg'].startswith("PT") and len(fiscalization['nº reg'].split("-")) != 3:
                print(fiscalization['nº reg'])
                print(index)

# Manually transform some mistakes
checked_fiscrep['nº reg'].iloc[6519] = 'PTCAM-116978-L'
checked_fiscrep['nº reg'].iloc[10426] = 'PTLOS-117532-L'
checked_fiscrep['nº reg'].iloc[10430] = 'PTCAM-113838-L'
checked_fiscrep['nº reg'].iloc[10445] = 'PTCAM-113838-L'

checked_fiscrep.to_pickle('checked_fiscrep.pickle')

# Just some few problems

ships_more_reg2 = ships_more_reg[ships_more_reg.num_regs>1]

regs_with_3 = []

for reg in CFR_data_cut['Registration Number']:
    reg = str(reg)
    if reg.startswith('3'):
        regs_with_3.append(reg)


regs_with_3 = list(set(regs_with_3))

ships_more_reg2['maximum_similaritie_CFR'] = 0

reg_lists = []

for reg in ships_more_reg2.alternative_reg:
    dist = []
    for reg2 in regs_with_3:
        temp_dist = fuzz.ratio(reg, reg2)
        dist.append(temp_dist)
    dist_max = np.max(dist)
    ships_more_reg2['maximum_similaritie_CFR'][ships_more_reg2.alternative_reg==reg] = dist_max
    if dist_max>85:
        print(reg)
        print(np.array(regs_with_3)[np.where(dist==dist_max)])
        reg_lists.append(np.array(regs_with_3)[np.where(dist==dist_max)])
    else:
        reg_lists.append([])

names_alternative = []

ships_more_reg2['similar_CFR'] = reg_lists

for i, row in ships_more_reg2.iterrows():
    if len(row.similar_CFR)>0:
        names = []
        for reg in row.similar_CFR:
            name = CFR_data_cut[CFR_data_cut['Registration Number']==reg]['Name of vessel'].unique()[0]
            names.append(name)
        names_alternative.append(names)
    else:
        names_alternative.append([])

ships_more_reg2['corresponding_names'] = names_alternative


    

ships_more_reg2.to_excel('ships_more_reg2.xlsx')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Alterate manually a
unchecked_fiscrep_manual = pd.read_excel('ships_more_reg_man_check.xlsx')

unchecked_fiscrep_manual = unchecked_fiscrep_manual.rename(columns={'Unnamed: 13': 'real_CFR_MAN', 'Unnamed: 12': 'replace'})

unchecked_fiscrep_manual = unchecked_fiscrep_manual[unchecked_fiscrep_manual['replace']==1]

unchecked_fiscrep['replace'] = 0

for i, fisc in unchecked_fiscrep.iterrows():
    Nome = fisc["Nome"]
    if Nome in unchecked_fiscrep_manual["Nome"].values:
        print(Nome)
        print(unchecked_fiscrep.Nome.loc[i])
        unchecked_fiscrep.CFR.loc[i] = unchecked_fiscrep_manual.loc[unchecked_fiscrep_manual["Nome"] == Nome].real_CFR_MAN.values[0]
        unchecked_fiscrep.loc[i, "replace"] = 1

unchecked_fiscrep_present = unchecked_fiscrep[unchecked_fiscrep['replace']==1]
unchecked_fiscrep_present.drop(columns='replace',inplace=True)
unchecked_fiscrep_present['True_CFR'] = 1

unchecked_fiscrep = unchecked_fiscrep[unchecked_fiscrep['replace']==0]

checked_fiscrep['True_CFR'] = 0

checked_fiscrep = pd.concat([checked_fiscrep, unchecked_fiscrep_present], ignore_index=True)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

checked_fiscrep.to_pickle('checked_fiscrep_2.pickle')
unchecked_fiscrep.to_excel('unchecked_fiscrep_2.xlsx')

