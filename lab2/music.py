import pandas as pd

def Q7():
    df = pd.read_csv("data/wmbr-cleaner.txt", delimiter = "|")
    df = df[['Artist','Song','Album']]
    live_songs = df[df['Song'].str.contains('live',case=False) | df['Album'].str.contains('live',case=False)]
    return sorted(live_songs['Artist'].unique(),key=lambda v: v.upper())

def Q8():
    df = pd.read_csv("data/wmbr-cleaner.txt", delimiter = "|")
    stranger_things = df[df['Album'].str.contains('stranger things',case=False)]
    return stranger_things[['DJ','Song']].groupby('DJ').count().sort_values('Song',ascending=False)

def Q9():
    df = pd.read_csv("data/wmbr-cleaner.txt", delimiter = "|")
    df['Year'] = df['Date'].str[-4:]
    df = df[df['Year'].isin(['2017','2018','2019'])]
    df['Billie'] = df['Artist'].str.contains('billie eilish',case=False)
    billie_songs = df[df['Billie']][['Song','Year']].groupby('Year').count()
    all_songs = df[['Song','Year']].groupby('Year').count()
    return (billie_songs/all_songs).sort_values('Year',ascending=False)

def Q10():
    lizzo = pd.read_json('data/lizzo_appearances.json')
    lizzo_years = lizzo[lizzo['Title'].str.contains('show',case=False)]['Year'].unique()

    df = pd.read_csv('data/wmbr-cleaner.txt', delimiter = '|')
    df['Year'] = df['Date'].str[-4:]
    df = df[df['Year'].isin(lizzo_years)]
    lizzo_songs = df[df['Artist'].str.contains('lizzo',case=False) | df['Song'].str.contains('lizzo',case=False)]
    return lizzo_songs['Song'].value_counts().reset_index().sort_values(['Song','index'],ascending=[False,True])

def Q11():
    wmbr = pd.read_csv('data/wmbr-cleaner.txt',delimiter='|')
    wmbr['Artist'] = wmbr['Artist'].str.split(',')
    wmbr['Artist'] = wmbr['Artist'].apply(lambda x: [val.strip() for val in x])
    wmbr['Artist'] = wmbr['Artist'].apply(lambda x: set(x))
    wmbr_artists = set.union(*wmbr['Artist'])

    top2018 = pd.read_csv('data/top2018.csv')
    top2018_wmbr = top2018[top2018['artists'].isin(wmbr_artists)]
    return top2018_wmbr.sort_values('danceability',ascending=False)[['name','artists','danceability']]

queries = [Q7,Q8,Q9,Q10,Q11]

for query in queries:
    print('\n' + query.__name__)
    print(query())
