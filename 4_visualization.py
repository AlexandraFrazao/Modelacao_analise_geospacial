import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with the counts of the variable by year
counts_df = df.groupby('Year')[variable].value_counts().unstack().fillna(0)
counts_df = counts_df.astype(int)

total_fiscs = counts_df.sum(axis=1).values
infracs_sel = counts_df.loc[:,1].values

# Calculate the proportion of the variable where it equals 1 per year
prop_df = infracs_sel/total_fiscs
prop_df = pd.Series(prop_df, index=counts_df.index)

# Create a bar plot using Seaborn
sns.barplot(x=prop_df.index, y=prop_df, color='blue')

# Set the title and axis labels
plt.title('Proportion of Infraction {} per Number of Registries per Year'.format(variable))
plt.xlabel('Year')
plt.ylabel('Proportion (%)')

# Show the plot
plt.show()



#to count the number of the fiscalization from witch PT16,....
import pandas as pd

df = pd.read_excel('final_fiscrep.xlsx')

# Count the occurrences of each NUTSII_code
nut_counts = df['NUTSII_code'].value_counts()

print(nut_counts)



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle('final_fiscrep.pickle')

# Filter the data by NUTSII_code and Result
df_filtered = df[(df['NUTSII_code'] == 'PT11') & (df['Result'] == 'PRESUM')]

# Create a countplot using Seaborn
sns.countplot(x=df_filtered['Year'], data=df_filtered)

# Set the title and axis labels
plt.title("Number of Infrac in NUTS II PT11")
plt.xlabel("Year")
plt.ylabel("Number of PRESUM Fiscalizations")

plt.show()



#### deu certo igual ao de cima mas com números nas barras

import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

# Load the Excel file into a Pandas DataFrame, skipping the first two rows
INE = pd.read_excel('INE.xlsx', sheet_name='Q1', skiprows=1)

# Extract the columns of interest
INE_subset = INE[['NUTSII_code', 'População_residente', 'População_empregada']]

# Set the NUTSII_code column as the index
INE_subset.set_index('NUTSII_code', inplace=True)

# Plot a bar plot of the DataFrame
INE_subset.plot(kind='bar')
plt.title('Population by NUTS II')
plt.xlabel('NUTS II code')
plt.ylabel('Population')

# Format the y-axis tick labels to display integers
plt.ticklabel_format(style='plain', axis='y')

# Add text labels to each bar
for i, v in enumerate(INE_subset.values):
    plt.text(i-0.15, v[0]+10000, str(v[0]), rotation=90, color='black', fontsize=10)
    plt.text(i+0.1, v[1]+10000, str(v[1]), rotation=90, color='black', fontsize=10)

plt.show()






import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

df = pd.read_pickle('final_fiscrep.pickle')

# Create a bar plot for total fiscalizations using Seaborn
ax = sns.countplot(x="NUTSII_code", data=df, color='blue')

# Add labels to the total fiscalizations plot
ax.set_title("Número de fiscalizações realizadas e resultado de PI por NUTS II")
ax.set_xlabel("NUTS II")
ax.set_ylabel("Número Total")

# Get the count of fiscalizations per 'NUTS' code
total_counts = df.groupby("NUTSII_code").size().reset_index(name="Total")

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Get the count of "PRESUM" fiscalizations per 'NUTS' code
presum_counts = df_presum.groupby("NUTSII_code").size().reset_index(name="Presumível Infrator")

# Merge the total and "PRESUM" counts based on 'NUTS' code
combined_df = pd.merge(total_counts, presum_counts, on="NUTSII_code", how="left").fillna(0)


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

df = pd.read_pickle('final_fiscrep.pickle')

# Get the count of fiscalizations per 'NUTSII_code'
total_counts = df.groupby("NUTSII_code").size().reset_index(name="Total")

# Display the total_counts DataFrame
print(total_counts)

# Create a bar plot for total fiscalizations using Seaborn
plt.figure(figsize=(8, 6))
sns.barplot(x="NUTSII_code", y="Total", data=total_counts, color='blue')

# Add labels to the plot
plt.title("Número de fiscalizações realizadas por NUTS II")
plt.xlabel("NUTS II")
plt.ylabel("Número Total")

# Adjust the layout to avoid overlapping labels
plt.tight_layout()

# Show the bar plot
plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

df = pd.read_pickle('final_fiscrep.pickle')

sns.set_style("whitegrid")
sns.set_palette("pastel")

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Group the original dataframe by year and count the total number of fiscalizations
df_total = df.groupby("Year")["Result"].count().reset_index()

# Merge the total fiscalizations dataframe with the PRESUM fiscalizations dataframe
df_merged = pd.merge(df_total, df_presum.groupby("Year")["Result"].count().reset_index(), on="Year")

# Calculate the proportion of PRESUM fiscalizations over the total fiscalizations
df_merged["Prop"] = df_merged["Result_y"] / df_merged["Result_x"]

# Create a line plot using Seaborn
sns.lineplot(x="Year", y="Prop", data=df_merged, color="blue")

# Set the title and axis labels
plt.title("Proporção de fiscalizações PI em relação ao total das fiscalizações por Ano")
plt.xlabel("Ano")
plt.ylabel("Proporção")

# Display the plot
plt.show()


para_nuts = pd.DataFrame(merged_df.NameWoDiacritics.unique())

para_nuts.to_excel('para_nuts.xlsx')


# Count unique 'matched_CFR' values
unique_matched_cfr_count = merged_df['matched_CFR'].nunique()
# Count unique 'matched_CFR' values with 'Result' equal to 'PRESUM'
presum_matched_cfr_count = merged_df.loc[merged_df['Result'] == 'PRESUM', 'matched_CFR'].nunique()

presum_vessels = merged_df[merged_df['Result'] == 'PRESUM']['Name']
print(presum_vessels)
duplicated_vessels = presum_vessels.value_counts().loc[lambda x: x > 1]
total_frequency = duplicated_vessels.sum()
print(duplicated_vessels)

import pandas as pd

presum_vessels = merged_df[merged_df['Result'] == 'PRESUM']['Name']
duplicated_vessels = presum_vessels.value_counts().loc[lambda x: x > 1]

# Create the table
table = pd.DataFrame({'Vessel Name': duplicated_vessels.index, 'Frequency': duplicated_vessels.values})
print(table)






#Artes de Pesca
#quantidade
artes_diferentes = merged_df['Gear'].nunique()
print("Número de artes diferentes: ", artes_diferentes)


#Year
gear_counts = merged_df['Gear'].value_counts()
gear_counts_presum = merged_df.loc[merged_df['Result'].str.contains('PRESUM'), 'Gear'].value_counts()
print(gear_counts)
print(gear_counts_presum)


#NUTSII
gear_counts_NUTS = merged_df.groupby(['Gear', 'NUTSII_code']).size()
gear_counts_presum_NUTS = merged_df.loc[merged_df['Result'].str.contains('PRESUM')].groupby(['Gear', 'NUTSII_code']).size()
print(gear_counts_NUTS)
print(gear_counts_presum_NUTS)


#descrição
artes_descricao = merged_df.groupby('Gear').describe()

columns_of_interest = ['LOA']
artes_descricao = merged_df.groupby(['Gear', 'Year'])[columns_of_interest].describe()
artes_descricao['Presum_Count'] = merged_df[merged_df['Result'] == 'PRESUM'].groupby(['Gear', 'Year']).size()
artes_descricao.reset_index(inplace=True)

artes_descricao.to_csv('artes_descricao.csv', index=False)
