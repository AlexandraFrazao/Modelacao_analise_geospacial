import pandas as pd

url = 'https://service.unece.org/trade/locode/pt.htm'
tables = pd.read_html(url)
df = tables[2].iloc[1:]
names_html = list(tables[2].iloc[0])

df = pd.DataFrame(df.values, columns=names_html)

df['LOCODE_T'] = [code.replace(" ","") for code in df.LOCODE]

# To save the table as a CSV file
df.to_csv('table_locais.csv', index=False)