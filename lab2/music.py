import pandas as pd

def Q7():
    df = pd.read_csv("data/wmbr-clean.txt", delimiter = "|")
    df.columns = ['Date','Artist','Song','Album','Label','Show','DJ']
    df = df[['Artist','Song']]
    live_songs = df[df['Song'].str.contains('live')]
    return sorted(live_songs['Artist'].unique(),key=lambda v: v.upper())

queries = [Q7]
if __name__ == "__main__":
    for query in queries:
        print(query())
