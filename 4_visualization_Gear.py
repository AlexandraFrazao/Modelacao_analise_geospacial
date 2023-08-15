#Barplot from each Gear per each NUTSII
import seaborn as sns
import matplotlib.pyplot as plt

merged_df = pd.read_pickle('final_fiscrep.pickle')

# Get the unique 'Gear' values
unique_gears = merged_df['Gear'].unique()

# Iterate over each unique 'Gear' and create a bar plot
for gear in unique_gears:
    gear_data = merged_df[merged_df['Gear'] == gear]
    gear_counts = gear_data['NUTSII_code'].value_counts().reset_index()
    gear_counts.columns = ['NUTSII_code', 'Count']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='NUTSII_code', y='Count', data=gear_counts)
    plt.xlabel('NUTSII_code')
    plt.ylabel('Count')
    plt.title(f'Bar Plot of Counts for Gear {gear}')
    plt.xticks(rotation=45)
    plt.show()


#Barplot from each NUTSII per each Gear
import seaborn as sns
import matplotlib.pyplot as plt

# Get the unique 'NUTSII_code' values
unique_nutsii_codes = merged_df['NUTSII_code'].unique()

# Iterate over each unique 'NUTSII_code' and create a bar plot
for nutsii_code in unique_nutsii_codes:
    nutsii_code_data = merged_df[merged_df['NUTSII_code'] == nutsii_code]
    gear_counts = nutsii_code_data['Gear'].value_counts().reset_index()
    gear_counts.columns = ['Gear', 'Count']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Gear', y='Count', data=gear_counts)
    plt.xlabel('Arte')
    plt.ylabel('Número total')
    plt.title(f'N.º total de ações de fiscalização por arte - {nutsii_code}')
    plt.xticks(rotation=45)
    plt.show()


import seaborn as sns
import matplotlib.pyplot as plt

# Get the unique 'NUTSII_code' values
unique_nutsii_codes = merged_df['NUTSII_code'].unique()

# Define a single color for all bars
bar_color = 'blue'

# Iterate over each unique 'NUTSII_code' and create a bar plot
for nutsii_code in unique_nutsii_codes:
    nutsii_code_data = merged_df[merged_df['NUTSII_code'] == nutsii_code]
    gear_counts = nutsii_code_data['Gear'].value_counts().reset_index()
    gear_counts.columns = ['Gear', 'Count']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Gear', y='Count', data=gear_counts, color=bar_color)
    plt.xlabel('Arte')
    plt.ylabel('Número total')
    plt.title(f'N.º total de ações de fiscalização por arte - NUTS {nutsii_code}')
    plt.xticks(rotation=45)

    # Add total counts on top of each bar
    for index, value in enumerate(gear_counts['Count']):
        plt.text(index, value, str(value), ha='center', va='bottom', fontweight='bold')

    plt.show()




import seaborn as sns
import matplotlib.pyplot as plt

# Get the unique 'NUTSII_code' values
unique_nutsii_codes = merged_df['NUTSII_code'].unique()

# Define colors for the bars
bar_color_ax1 = 'blue'
bar_color_ax2 = 'red'

# Iterate over each unique 'NUTSII_code' and create a bar plot
for nutsii_code in unique_nutsii_codes:
    nutsii_code_data = merged_df[merged_df['NUTSII_code'] == nutsii_code]
    
    # Count and sum the rows with 'PRESUM' in the 'Result' column
    gear_counts = nutsii_code_data['Gear'].value_counts().reset_index()
    gear_counts.columns = ['Gear', 'Count']
    
    presum_counts = nutsii_code_data[nutsii_code_data['Result'] == 'PRESUM']['Gear'].value_counts().reset_index()
    presum_counts.columns = ['Gear', 'Presum_Count']
    
    gear_counts = gear_counts.merge(presum_counts, on='Gear', how='left')
    gear_counts['Presum_Count'].fillna(0, inplace=True)
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Gear', y='Count', data=gear_counts, color=bar_color_ax1)
    ax2 = ax.twinx()  # Create a second y-axis sharing the same x-axis
    sns.barplot(x='Gear', y='Presum_Count', data=gear_counts, ax=ax2, color=bar_color_ax2)

    # Set the labels and titles
    ax.set_xlabel('Arte')
    ax.set_ylabel('Número total')
    ax2.set_ylabel('Número total PRESUM', color=bar_color_ax2)
    ax.set_title(f'N.º total de ações de fiscalização por arte - NUTS {nutsii_code}')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Add total counts on top of each bar in ax1
    for index, value in enumerate(gear_counts['Count']):
        ax.text(index, value, str(value), ha='center', va='bottom', fontweight='bold')

    # Add total counts on top of each bar in ax2
    for index, value in enumerate(gear_counts['Presum_Count']):
        ax2.text(index, value, str(value), ha='center', va='bottom', fontweight='bold', color=bar_color_ax2)

    plt.show()



#TOTAL E PI, ARTES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the style as "whitegrid" to remove the gray background
sns.set_style("whitegrid")

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Lista com a ordem desejada dos valores da coluna 'Gear'
order = ['DRB', 'FPO', 'GNS', 'GTR', 'LHP', 'LLD', 'LLS', 'OTB', 'PS', 'TBB']

# Count total fiscalizations for each gear across all years
total_counts = df['Gear'].value_counts().reset_index()
total_counts.columns = ['Gear', 'Total']

# Count PRESUM fiscalizations for each gear across all years
presum_counts = df_presum['Gear'].value_counts().reset_index()
presum_counts.columns = ['Gear', 'Presum_Total']

# Sort the 'Gear' column based on the custom order
total_counts['Gear'] = pd.Categorical(total_counts['Gear'], categories=order)
total_counts.sort_values('Gear', inplace=True)

# Sort the 'Gear' column in the same order for the 'presum_counts' dataframe
presum_counts['Gear'] = pd.Categorical(presum_counts['Gear'], categories=order)
presum_counts.sort_values('Gear', inplace=True)

# Mesclar as contagens e preencher com 0
gear_counts = pd.merge(total_counts, presum_counts, on='Gear', how='left')
gear_counts.fillna(0, inplace=True)

# Create a bar plot for total fiscalizations (ax)
ax = sns.barplot(x="Gear", y="Total", data=gear_counts, color='blue', width=0.5)
ax.set_title("Número total de fiscalizações realizadas por Arte")
ax.set_xlabel("Arte")
ax.set_ylabel("Número Total")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Create a bar plot for PRESUM fiscalizations (ax2)
ax2 = ax.twinx()
sns.barplot(x="Gear", y="Presum_Total", data=gear_counts, ax=ax2, color="red", width=0.5)
ax2.set_ylabel("Presumível Infrator", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Annotate each bar with its value for total fiscalizations plot (ax)
for p in ax.patches:
    ax.annotate(format(p.get_height()),
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center',
                xytext=(0, 9), 
                textcoords='offset points')

# Annotate each bar with its value for PRESUM fiscalizations plot (ax2)
for p in ax2.patches:
    ax2.annotate(format(p.get_height()),
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='center',
                 xytext=(0, 9),
                 textcoords='offset points')

# Set the same y-axis limits for both plots
ax.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))
ax2.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))

# Display the plot
plt.tight_layout()
plt.show()




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the style as "whitegrid" to remove the gray background
sns.set_style("whitegrid")

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Get unique years
unique_years = df["Year"].unique()

# Lista com a ordem desejada dos valores da coluna 'Gear'
order = ['DRB', 'FPO', 'GNS', 'GTR', 'LHP', 'LLD', 'LLS', 'OTB', 'PS', 'TBB']

# Create a bar plot for each year
for year in unique_years:
    plt.figure(figsize=(8, 6))

    # Filter data for the current year
    year_data = df[df["Year"] == year]
    year_data_presum = df_presum[df_presum["Year"] == year]

    # Count total fiscalizations for each gear for the current year
    total_counts = year_data['Gear'].value_counts().reset_index()
    total_counts.columns = ['Gear', 'Total']

    # Count PRESUM fiscalizations for each gear for the current year
    presum_counts = year_data_presum['Gear'].value_counts().reset_index()
    presum_counts.columns = ['Gear', 'Presum_Total']

    # Sort the 'Gear' column based on the custom order
    total_counts['Gear'] = pd.Categorical(total_counts['Gear'], categories=order)
    total_counts.sort_values('Gear', inplace=True)
    
    # Sort the 'Gear' column in the same order for the 'presum_counts' dataframe
    presum_counts['Gear'] = pd.Categorical(presum_counts['Gear'], categories=order)
    presum_counts.sort_values('Gear', inplace=True)

    # Mesclar as contagens e preencher com 0
    gear_counts = pd.merge(total_counts, presum_counts, on='Gear', how='left')
    gear_counts.fillna(0, inplace=True)

    # Create a bar plot for total fiscalizations for the current year (ax)
    ax = sns.barplot(x="Gear", y="Total", data=gear_counts, color='blue', width=0.5)
    ax.set_title(f"Número de fiscalizações realizadas por Arte em {year}", fontsize=16)
    ax.set_xlabel("Arte", fontsize=14)
    ax.set_ylabel("Número Total", fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Create a bar plot for PRESUM fiscalizations for the current year (ax2)
    ax2 = ax.twinx()
    sns.barplot(x="Gear", y="Presum_Total", data=gear_counts, ax=ax2, color="red", width=0.5)
    ax2.set_ylabel("Presumível Infrator", color="red", fontsize=14)
    ax2.tick_params(axis="y", labelcolor="red")

    # Annotate each bar with its value for total fiscalizations plot (ax)
    for p in ax.patches:
        ax.annotate(format(p.get_height()),
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center',
                    xytext=(0, 9), 
                    textcoords='offset points')

    # Annotate each bar with its value for PRESUM fiscalizations plot (ax2)
    for p in ax2.patches:
        ax2.annotate(format(p.get_height()),
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='center',
                     xytext=(0, 9),
                     textcoords='offset points')

    # Set the same y-axis limits for both plots
    ax.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))
    ax2.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))

    # Display the plot
    plt.tight_layout()
    plt.show()






import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

sns.set_style("whitegrid")

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Get unique years
unique_years = df["Year"].unique()

# Create a line plot for the proportion by gear for each year
for year in unique_years:
    plt.figure(figsize=(8, 6))
    
    # Filter data for the current year
    year_data = df[df["Year"] == year]
    year_data_presum = df_presum[df_presum["Year"] == year]
    
    # Create a DataFrame with all possible gears
    all_gears = df['Gear'].unique()
    gear_df = pd.DataFrame({'Gear': all_gears})
    
    # Merge the gear DataFrame with the year data to include missing gears
    proportion_data = pd.merge(gear_df, year_data, on='Gear', how='left')
    
    # Calculate the proportion for each gear
    proportion_data['Presum_Total'] = proportion_data['Result'].eq('PRESUM').groupby(proportion_data['Gear']).transform('sum')
    proportion_data['Total'] = proportion_data['Result'].groupby(proportion_data['Gear']).transform('count')
    proportion_data['Proportion'] = proportion_data['Presum_Total'] / proportion_data['Total']
    
    # Sort the DataFrame by the gear name to ensure consistent order
    proportion_data.sort_values(by='Gear', inplace=True)
    
    # Create a line plot for the proportion by gear using Seaborn
    sns.lineplot(x='Gear', y='Proportion', data=proportion_data, marker='o', palette='bright')
    plt.title(f"Rácio de Presumíveis Infratores por Arte em {year}", fontsize=16)
    plt.xlabel("Arte", fontsize=14)
    plt.ylabel("Rácio de Presumíveis Infratores", fontsize=14)
    plt.xticks(rotation=45)
    
    # Annotate each point with its value
    for x, y in zip(proportion_data['Gear'], proportion_data['Proportion']):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
    
    # Annotate each point with its total fiscalizations count on ax
    for x, y in zip(proportion_data['Gear'], proportion_data['Total']):
        plt.text(x, y, f'{y}', ha='center', va='bottom', color='blue')
    
    # Annotate each point with its total fiscalizations presumíveis count on ax2
    for x, y in zip(proportion_data['Gear'], proportion_data['Presum_Total']):
        plt.text(x, y, f'{y}', ha='center', va='bottom', color='red')
    
    plt.tight_layout()
    plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the style as "whitegrid" to remove the gray background
sns.set_style("whitegrid")

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Get unique NUTSII_codes
unique_nutsii_codes = df["NUTSII_code"].unique()

# Lista com a ordem desejada dos valores da coluna 'Gear'
order = ['DRB', 'FPO', 'GNS', 'GTR', 'LHP', 'LLD', 'LLS', 'OTB', 'PS', 'TBB']

# Create a bar plot for each NUTSII_code
for nutsii_code in unique_nutsii_codes:
    plt.figure(figsize=(8, 6))
    
    # Filter data for the current NUTSII_code
    nutsii_code_data = df[df["NUTSII_code"] == nutsii_code]
    nutsii_code_data_presum = df_presum[df_presum["NUTSII_code"] == nutsii_code]

    # Count total fiscalizations for each gear for the current NUTSII_code
    total_counts = nutsii_code_data['Gear'].value_counts().reset_index()
    total_counts.columns = ['Gear', 'Total']

    # Count PRESUM fiscalizations for each gear for the current NUTSII_code
    presum_counts = nutsii_code_data_presum['Gear'].value_counts().reset_index()
    presum_counts.columns = ['Gear', 'Presum_Total']

    # Sort the 'Gear' column based on the custom order
    total_counts['Gear'] = pd.Categorical(total_counts['Gear'], categories=order)
    total_counts.sort_values('Gear', inplace=True)

    # Sort the 'Gear' column in the same order for the 'presum_counts' dataframe
    presum_counts['Gear'] = pd.Categorical(presum_counts['Gear'], categories=order)
    presum_counts.sort_values('Gear', inplace=True)

    # Merge the two counts on 'Gear' column
    gear_counts = pd.merge(total_counts, presum_counts, on='Gear', how='left')
    gear_counts.fillna(0, inplace=True)

    # Create a bar plot for total fiscalizations for the current NUTSII_code (ax)
    ax = sns.barplot(x="Gear", y="Total", data=gear_counts, color='blue', width=0.5)
    ax.set_title(f"Número de fiscalizações realizadas por Arte na NUTS II {nutsii_code}", fontsize=16)
    ax.set_xlabel("Arte", fontsize=14)
    ax.set_ylabel("Número Total", fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Create a bar plot for PRESUM fiscalizations for the current NUTSII_code (ax2)
    ax2 = ax.twinx()
    sns.barplot(x="Gear", y="Presum_Total", data=gear_counts, ax=ax2, color="red", width=0.5)
    ax2.set_ylabel("Presumível Infrator", color="red", fontsize=14)
    ax2.tick_params(axis="y", labelcolor="red")

    # Annotate each bar with its value for total fiscalizations plot (ax)
    for p in ax.patches:
        ax.annotate(format(p.get_height()),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom',
                    xytext=(0, 9),
                    textcoords='offset points')

    # Annotate each bar with its value for PRESUM fiscalizations plot (ax2)
    for p in ax2.patches:
        ax2.annotate(format(p.get_height()),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom',
                     xytext=(0, 9),
                     textcoords='offset points')

    # Set the same y-axis limits for both plots
    ax.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))
    ax2.set_ylim(0, max(ax.get_ylim()[1], ax2.get_ylim()[1]))

    # Display the plot
    plt.tight_layout()
    plt.show()





#RÁCIO PI/TOTAL
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the inline display for Jupyter or other similar environments
%matplotlib inline

# Define the style as "whitegrid" to remove the gray background
sns.set_style("whitegrid")

df = pd.read_pickle('final_fiscrep.pickle')

# Create a new dataframe with only "PRESUM" fiscalizations
df_presum = df[df["Result"] == "PRESUM"]

# Get unique NUTSII_codes
unique_nutsii_codes = df["NUTSII_code"].unique()

# Lista com a ordem desejada dos valores da coluna 'Gear'
order = ['DRB', 'FPO', 'GNS', 'GTR', 'LHP', 'LLD', 'LLS', 'OTB', 'PS', 'TBB']

# Create a line plot for each NUTSII_code
for nutsii_code in unique_nutsii_codes:
    plt.figure(figsize=(8, 6))
    
    # Filter data for the current NUTSII_code
    nutsii_code_data = df[df["NUTSII_code"] == nutsii_code]
    nutsii_code_data_presum = df_presum[df_presum["NUTSII_code"] == nutsii_code]
    
    # Count total fiscalizations for each gear for the current NUTSII_code
    total_counts = nutsii_code_data['Gear'].value_counts().reindex(order).reset_index()
    total_counts.columns = ['Gear', 'Total']
    
    # Count PRESUM fiscalizations for each gear for the current NUTSII_code
    presum_counts = nutsii_code_data_presum['Gear'].value_counts().reindex(order).reset_index()
    presum_counts.columns = ['Gear', 'Presum_Total']
    
    # Merge the two counts on 'Gear' column
    gear_counts = pd.merge(total_counts, presum_counts, on='Gear', how='left')
    gear_counts.fillna(0, inplace=True)
    
    # Calculate the proportion PRESUM/Total for each gear
    gear_counts['Proportion'] = gear_counts['Presum_Total'] / gear_counts['Total']
    
    # Create a line plot for proportion PRESUM/Total for the current NUTSII_code
    ax = sns.lineplot(x="Gear", y="Proportion", data=gear_counts, marker='o', color='blue')
    ax.set_title(f"Rácio de PI/Total ações fiscalização por Arte na NUTS II {nutsii_code}", fontsize=16)
    ax.set_xlabel("Arte", fontsize=14)
    ax.set_ylabel("Rácio", fontsize=14)
    ax.set_xticklabels(gear_counts['Gear'], rotation=45)
    
    # Annotate each point with its value for proportion PRESUM/Total plot
    for x, y in zip(gear_counts['Gear'], gear_counts['Proportion']):
        ax.annotate(format(y, '.2f'), (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    # Display the plot
    plt.tight_layout()
    plt.show()







