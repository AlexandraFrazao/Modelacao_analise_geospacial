import matplotlib.pyplot as plt
import pandas as pd

merged_df = pd.read_pickle('final_fiscrep.pickle')
df = pd.read_pickle('final_fiscrep.pickle')

# Plotting the histogram
plt.hist(df['LOA'])

# Getting the counts for each bin
counts, bins, _ = plt.hist(df['LOA'], color='blue')

# Adding text above each column
for count, x in zip(counts, bins):
    plt.text(x + 0.5, count + 5, str(int(count)), ha='center', fontsize=8, va='bottom')

# Adding labels and title
plt.xlabel('LOA (metros)')
plt.ylabel('Frequência')
plt.title('LOA - FISCREP')

plt.xticks(fontsize=8)

# Displaying the plot
plt.show()

loa_description = merged_df['LOA'].describe()




import pandas as pd
import matplotlib.pyplot as plt

selected_df = merged_df[['matched_CFR', 'LOA']]

# Drop duplicates for each unique combination of 'matched_CFR' and 'LOA'
unique_loa_per_cfr = selected_df.drop_duplicates(subset=['matched_CFR', 'LOA'], keep='first')

# Count the unique 'CFR' values after dropping duplicates
cfr_counts = unique_loa_per_cfr['matched_CFR'].nunique()

# Create the histogram for 'LOA' values
plt.hist(unique_loa_per_cfr['LOA'], bins=10, color='blue')

# Add text for the total number of unique 'CFR' values above the histogram
# Adding text above each column
for count, x in zip(cfr_counts, range(1, len(cfr_counts)+1)):
    plt.text(x, count + 5, f'Total CFR: {count}', ha='center')

# Adding labels and title
plt.xlabel('LOA (metros)')
plt.ylabel('Frequência')
plt.title('Distribuição LOA por embarcações únicas')

plt.xticks(fontsize=8)
 
# Displaying the plot
plt.tight_layout()
plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# Assume that 'merged_df' is already defined
selected_df = merged_df[['matched_CFR', 'LOA', 'Year']]

# Group data by year and calculate the mean 'LOA' for each year
mean_loa_by_year = selected_df.groupby('Year')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='Year', y='LOA', data=mean_loa_by_year, marker='o', color='blue')
plt.title('Média LOA em metros por Ano', fontsize= 18)
plt.xlabel('Ano', fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year['Year'], mean_loa_by_year['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()






#MEAN LOA & PI & YEAR
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# Assume that 'merged_df' is already defined
selected_df = merged_df[merged_df['Result'] == 'PRESUM'][['matched_CFR', 'LOA', 'Year']]
selected_df.describe()

# Group data by year and calculate the mean 'LOA' for each year
mean_loa_by_year = selected_df.groupby('Year')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='Year', y='LOA', data=mean_loa_by_year, marker='o', color='blue')
plt.title('Média LOA em metros por Ano - Resultado PI', fontsize= 18)
plt.xlabel('Ano', , fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year['Year'], mean_loa_by_year['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()


#Média LOA em metros por embarcações únicas - Ano
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

selected_df = merged_df[['matched_CFR', 'LOA', 'Year']]

# Drop duplicates for each unique combination of 'matched_CFR' and 'LOA'
unique_loa_per_cfr = selected_df.drop_duplicates(subset=['matched_CFR', 'LOA'], keep='first')

# Count the unique 'CFR' values after dropping duplicates
cfr_counts = unique_loa_per_cfr['matched_CFR'].nunique()

# Group data by year and calculate the mean 'LOA' for each year
mean_loa_by_year = unique_loa_per_cfr.groupby('Year')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='Year', y='LOA', data=mean_loa_by_year, marker='o', color='blue')
plt.title('Média LOA em metros por embarcações únicas - Ano', fontsize= 18)
plt.xlabel('Ano', fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year['Year'], mean_loa_by_year['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# Add a text annotation for the number of unique 'CFR' values
plt.annotate(f"Número de CFRs únicos: {cfr_counts}", 
             xy=(0.95, 0.9), xycoords='axes fraction', 
             ha='right', fontsize=10, color='gray')

plt.tight_layout()
plt.show()


#Média LOA em metros por embarcações únicas por Ano - Resultado PI
selected_df = merged_df[merged_df['Result'] == 'PRESUM'][['matched_CFR', 'LOA', 'Year']]
selected_df.describe()

# Drop duplicates for each unique combination of 'matched_CFR' and 'LOA' where 'Result' is 'PRESUM'
unique_loa_per_cfr_presum = selected_df.drop_duplicates(subset=['matched_CFR', 'LOA'], keep='first')

# Count the unique 'CFR' values after dropping duplicates
cfr_counts_presum = unique_loa_per_cfr_presum['matched_CFR'].nunique()

# Group data by year and calculate the mean 'LOA' for each year where 'Result' is 'PRESUM'
mean_loa_by_year_presum = unique_loa_per_cfr_presum.groupby('Year')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='Year', y='LOA', data=mean_loa_by_year_presum, marker='o', color='blue')
plt.title('Média LOA em metros por embarcações únicas por Ano - Resultado PI', fontsize= 18)
plt.xlabel('Ano', fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year_presum['Year'], mean_loa_by_year_presum['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()



#Média LOA em metros por NUTS II
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# Assume that 'merged_df' is already defined
selected_df = merged_df[['matched_CFR', 'LOA', 'NUTSII_code']]

# Group data by year and calculate the mean 'LOA' for each year
mean_loa_by_year = selected_df.groupby('NUTSII_code')['LOA'].mean().reset_index()

# Set the style to display grid lines
sns.set(style="whitegrid")

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='NUTSII_code', y='LOA', data=mean_loa_by_year, marker='o', color='blue')
plt.title('Média LOA em metros por NUTS II', fontsize= 18)
plt.xlabel('NUTS II', fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)

plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year['NUTSII_code'], mean_loa_by_year['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()


#Média LOA em metros por NUTS II - Resultado PI
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

selected_df = merged_df[merged_df['Result'] == 'PRESUM'][['matched_CFR', 'LOA', 'NUTSII_code']]

# Group data by year and calculate the mean 'LOA' for each year
mean_loa_by_year = selected_df.groupby('NUTSII_code')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by year
plt.figure(figsize=(9, 6))
sns.lineplot(x='NUTSII_code', y='LOA', data=mean_loa_by_year, marker='o', color='blue')
plt.title('Média LOA em metros por NUTS II - Resultado PI', fontsize= 18)
plt.xlabel('NUTS II', fontsize= 16)
plt.ylabel('Média LOA (metros)', fontsize= 16)

plt.xticks(rotation=45)

# Annotate each point with its value
for x, y in zip(mean_loa_by_year['NUTSII_code'], mean_loa_by_year['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.show()




#UNIQUE_NUTSII
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# Assume that 'merged_df' is already defined
selected_df = merged_df[['matched_CFR', 'LOA', 'NUTSII_code']]

# Drop duplicates for each unique combination of 'matched_CFR' and 'NUTSII_code'
unique_loa_per_cfr_nutsii = selected_df.drop_duplicates(subset=['matched_CFR', 'NUTSII_code'], keep='first')

# Count the unique 'NUTSII_code' values after dropping duplicates
nutsii_counts = unique_loa_per_cfr_nutsii['NUTSII_code'].nunique()

# Group data by 'NUTSII_code' and calculate the mean 'LOA' for each 'NUTSII_code'
mean_loa_by_nutsii = unique_loa_per_cfr_nutsii.groupby('NUTSII_code')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by 'NUTSII_code'
plt.figure(figsize=(9, 6))
sns.lineplot(x='NUTSII_code', y='LOA', data=mean_loa_by_nutsii, marker='o', color='blue')
plt.title('Média LOA em metros das embarcações únicas por NUTS II', fontsize= 18)
#plt.xlabel('Número de NUTSII_code únicos')
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)
plt.xlabel('NUTS II', fontsize= 16)

# Annotate each point with its value
for x, y in zip(mean_loa_by_nutsii['NUTSII_code'], mean_loa_by_nutsii['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.tight_layout()
plt.show()


#UNIQUE_NUTSII_PI
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# Assume that 'merged_df' is already defined
selected_df = merged_df[merged_df['Result'] == 'PRESUM'][['matched_CFR', 'LOA', 'NUTSII_code']]

# Drop duplicates for each unique combination of 'matched_CFR' and 'NUTSII_code'
unique_loa_per_cfr_nutsii = selected_df.drop_duplicates(subset=['matched_CFR', 'NUTSII_code'], keep='first')

# Count the unique 'NUTSII_code' values after dropping duplicates
nutsii_counts = unique_loa_per_cfr_nutsii['NUTSII_code'].nunique()

# Group data by 'NUTSII_code' and calculate the mean 'LOA' for each 'NUTSII_code'
mean_loa_by_nutsii = unique_loa_per_cfr_nutsii.groupby('NUTSII_code')['LOA'].mean().reset_index()

# Create a line plot for the mean 'LOA' by 'NUTSII_code'
plt.figure(figsize=(9, 6))
sns.lineplot(x='NUTSII_code', y='LOA', data=mean_loa_by_nutsii, marker='o', color='blue')
plt.title('Média LOA em metros das embarcações únicas PI por NUTS II', fontsize= 18)
#plt.xlabel('Número de NUTSII_code únicos')
plt.ylabel('Média LOA (metros)', fontsize= 16)
plt.xticks(rotation=45)
plt.xlabel('NUTS II', fontsize= 16)

# Annotate each point with its value
for x, y in zip(mean_loa_by_nutsii['NUTSII_code'], mean_loa_by_nutsii['LOA']):
    plt.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.tight_layout()
plt.show()




# Filtering the DataFrame for rows where 'security' column has the value 'S'
security_s = df[df['security'] == 'S']

# Counting the number of 'S' values in 'security' column grouped by 'Year'
security_counts = security_s.groupby('Year').size()

# Filtering the DataFrame for rows where 'fishery' column has the value 'P'
fishery_p = df[df['fishery'] == 'P']

# Counting the number of 'P' values in 'fishery' column grouped by 'Year'
fishery_counts = fishery_p.groupby('Year').size()

# Merging the counts into one DataFrame
count_df = pd.DataFrame({
    'Segurança': security_counts,
    'Pescas': fishery_counts
}).fillna(0)  # filling NaN values with 0

ax = count_df.plot(kind='bar', figsize=(10,6))

plt.title('Número total de Infrações: Segurança e Pescas por Ano')
plt.ylabel('Número total')
plt.xlabel('Ano')
plt.tight_layout()
plt.legend(loc='upper right')

# Adding the total number above each bar
for p in ax.patches:
    ax.annotate(str(int(p.get_height())), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.show()


# Calculate the total counts per year
count_df['total'] = count_df['Segurança'] + count_df['Pescas']

# Convert the counts to proportions
count_df['Segurança'] = count_df['Segurança'] / count_df['total'] * 100
count_df['Pescas'] = count_df['Pescas'] / count_df['total'] * 100

# Drop the total column as it's no longer needed
count_df.drop('total', axis=1, inplace=True)

# Plotting using a line plot
ax = count_df.plot(kind='line', marker='o', figsize=(10,6))

plt.title('Proporção de Infrações: Segurança e Pescas por Ano')
plt.ylabel('Percentagem (%)')
plt.xlabel('Ano')
plt.tight_layout()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='upper right')

# Extract the x-ticks (years) from the plot for accurate placement
xticks = ax.get_xticks()

# Annotations
for year, row in count_df.iterrows():
    if year in xticks:  # only annotate for the years that are in the xticks
        plt.text(year, row['Segurança'] + 1, '{:.1f}%'.format(row['Segurança']), ha='center', fontsize=10)
        plt.text(year, row['Pescas'] - 3, '{:.1f}%'.format(row['Pescas']), ha='center', fontsize=10)

# Adjust y-axis limits to fit annotations
ylim = ax.get_ylim()
ax.set_ylim(min(ylim[0], count_df['Pescas'].min() - 5), max(ylim[1], count_df['Segurança'].max() + 5))

plt.show()















# Filtering and counting for 'security' column
security_s = df[df['security'] == 'S']
security_counts = security_s.groupby('NUTSII_code').size()

# Filtering and counting for 'fishery' column
fishery_p = df[df['fishery'] == 'P']
fishery_counts = fishery_p.groupby('NUTSII_code').size()

# Merging the counts into one DataFrame
count_df = pd.DataFrame({
    'Segurança': security_counts,
    'Pescas': fishery_counts
}).fillna(0)  # filling NaN values with 0

# Plotting
ax = count_df.plot(kind='bar', figsize=(10,6))

plt.title('Número total de Infrações: Segurança e Pescas por NUTS II')
plt.ylabel('Número Total')
plt.xlabel('NUTS II')
plt.tight_layout()
plt.legend(loc='upper right')

# Adding the total number above each bar
for p in ax.patches:
    ax.annotate(str(int(p.get_height())), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.show()

# Convert the counts to proportions
count_df['total'] = count_df['Segurança'] + count_df['Pescas']
count_df['Segurança'] = count_df['Segurança'] / count_df['total'] * 100
count_df['Pescas'] = count_df['Pescas'] / count_df['total'] * 100

# Drop the total column as it's no longer needed
count_df.drop('total', axis=1, inplace=True)

# Plotting
ax = count_df.plot(kind='line', marker='o', figsize=(10,6))

plt.title('Proporção de Infrações: Segurança e Pescas por NUTS II')
plt.ylabel('Percentagem (%)')
plt.xlabel('NUTS II')
plt.tight_layout()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='upper right')

for i, row in enumerate(count_df.iterrows()):
    plt.text(i, row[1]['Segurança'] + 1, '{:.1f}%'.format(row[1]['Segurança']), ha='center')
    plt.text(i, row[1]['Pescas'] - 3, '{:.1f}%'.format(row[1]['Pescas']), ha='center')

plt.show()






