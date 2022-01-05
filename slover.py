#! /opt/conda/bin/python
import pandas as pd
import re

# %%
df = pd.read_csv('dataset.csv', index_col=0)
normalized_df = (df-df.mean())/df.std()
weights = [1, 5, 1]
normalized_df['score'] = normalized_df.dot(weights)
words = normalized_df.sort_values('score', ascending=False)
words.to_csv('words.csv')


def remove_word_from_dataset(word):
    df = pd.read_csv('dataset.csv', index_col=0)
    df.drop(word).to_csv('dataset.csv')


# %%
words = pd.read_csv('words.csv', index_col=0)

# %%


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

# %%


def get_regex_of_result(guess, result, symbol):
    regex = '^.....$'
    for m in find(result, symbol):
        regex = regex[:m+1] + guess[m] + regex[m + 2:]
    return regex

# %%


def remove_not_in_word(words, guess, result):
    df = words.copy()
    indexs = find(result, '-')
    for i in indexs:
        df = df[~df.index.str.contains(guess[i])]
        if len(df) == 0:
            return df
    return df

# %%


def remove_not_in_place(words, guess, result):
    df = words.copy()
    symbol = '+'
    indexs = find(result, symbol)

    for i in indexs:
        df = df[df.index.str.contains(guess[i])]
        if len(df) == 0:
            return df
        regex = '^.....$'
        regex = regex[:i+1] + guess[i] + regex[i + 2:]
        df = df[~df.index.str.contains(regex)]
        if len(df) == 0:
            return df
    return df

# %%


def remove_in_place(words, guess, result):
    df = words.copy()
    regex = get_regex_of_result(guess, result, '*')
    return df[df.index.str.contains(regex)]


# %%
words = pd.read_csv('words.csv', index_col=0)
while len(words) > 1:
    guess = words.index[0]
    print('my guess is:', guess)
    result = ''
    pattern = re.compile('^[\*\+\-]{5}$')
    while not pattern.match(result):
        result = input(
            'Enter result (* - char inplace, + - in word not place, - - char not in word): ')
        if result == 'remove':
            remove_word_from_dataset(guess)
            words.drop(guess, inplace=True)
            guess = words.index[0]
            print('my guess is:', guess)
    if result == '*'*5:
        break
    words = remove_not_in_word(words, guess, result)
    words = remove_in_place(words, guess, result)
    words = remove_not_in_place(words, guess, result)
    print(len(words), 'words left')
if len(words) == 0:
    print('did not find')
else:
    print(words.index[0], 'is the word')

# %%
