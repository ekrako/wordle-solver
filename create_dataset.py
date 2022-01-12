#! /opt/conda/bin/python
# %%
import pandas as pd
import string
la = pd.read_csv('all.csv', index_col=0)

# %%
df = la['0'].apply(lambda x: pd.Series(list(x)))

# %%
alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)
counts = pd.DataFrame(index=alphabet_list)
for col in df.columns:
    counts[col] = df[col].value_counts()
counts.fillna(0, inplace=True)

# %%
freq = counts/len(df)

# %%
x = la['0'][0]

# %%
la['freq'] = la['0'].apply(lambda x: sum(freq[i][v] for i, v in enumerate(x)))
la['unique'] = la['0'].apply(lambda x: len(set(x)))

# %%
la = la.sort_values(by=['unique', 'freq'], ascending=False)
la = la.set_index('0')


# %%
la.to_csv('dataset.csv')
