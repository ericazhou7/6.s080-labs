import pandas as pd
import numpy as np
import argparse
import sklearn as skl
import score
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# You can add functions, and imports as neccesary for your ER algorithm
# you may find the scoring code useful for training and running locally

def run(directory):
    r1 = pd.read_csv(os.path.join(directory, "retailer1.csv"))
    r2 = pd.read_csv(os.path.join(directory, "retailer2.csv"))
    # TODO: This function should produce a csv file in the lab_3
    # directory using the name given by the follwing variable
    # e.g. "test_output.csv" for the test set. with the same format 
    # as data/train/matches.csv including the header
    # Please do not modify the output_filename
    output_filename = "test_output.csv"
    r3 = matching(r1, r2)
    r3.astype(dtype={"id1":int, "id2":int}).to_csv(output_filename, columns=["id1","id2"], index=False)


def train(directory):
    train_matches = pd.read_csv(os.path.join(directory, "matches.csv"))
    r1 = pd.read_csv(os.path.join(directory, "retailer1.csv"))
    r2 = pd.read_csv(os.path.join(directory, "retailer2.csv"))
    
    # TODO: This function should produce a csv file in the lab_3
    # directory named train_output.csv with the same format 
    # as data/train/matches.csv including the header
    # Please do not modify the output_filename
    output_filename = "train_output.csv"
    r3 = matching(r1, r2)
    r3.astype(dtype={"id1":int, "id2":int}).to_csv(output_filename, columns=["id1","id2"], index=False)

def matching(r1, r2):
    r1.modelno = r1.modelno.str.replace("[-\s]", "", regex=True).str.lower().replace(r"^/s*$", np.nan, regex=True)
    r2.modelno = r2.modelno.str.replace("[-\s]", "", regex=True).str.lower().replace(r"^/s*$", np.nan, regex=True)    
    
    vectorizer = TfidfVectorizer(min_df=1, binary=True) 
    s1 = (r1.groupname.map(str) + " " + r1.title.map(str) + " " +
          r1.brand.map(str) + " " +
          r1.modelno.map(str)).str.lower().replace("-", "", regex=False)
    
    s2 = (r2.pcategory1.map(str) + " "+ r2.pcategory2.map(str) + 
          " " + r2.title.map(str) + " " + r2.brand.map(str) + " " +
          r2.modelno.map(str)).str.lower().replace("-", "", regex=False)
    
    # build shared vocabulary
    tokenizer = vectorizer.build_tokenizer()
    s1_words = set(tokenizer(" ".join(s1.values)))
    s2_words = set(tokenizer(" ".join(s2.values)))
    vocabulary = {v:i for i,v in enumerate(s1_words.intersection(s2_words))}
        
    s3 = pd.concat([s2, s1])
    X = vectorizer.set_params(vocabulary=vocabulary).fit_transform(s3)
    s2_rows = s2.shape[0]
    match = X[:s2_rows].dot(X[s2_rows:].T)
    
    idx = np.argmax(match, axis=1)
    
    r1_idx = idx.A1
    r1_scores = np.amax(match, axis=1).toarray().reshape(-1)
    
    id1 = r1.iloc[r1_idx]["custom_id"].values
    id2 = r2.custom_id.values
    tot = np.array([id1, id2, r1_scores]).T
    df_bag = pd.DataFrame(tot, columns=["id1_bag", "id2", "score"])
    
    modelnos = set(r1.loc[r1.modelno.str.len() > 3, "modelno"].unique())
    idx_to_modelno = {i:word for word, i in vocabulary.items() if word in modelnos}
    select_idx = [0] + list(idx_to_modelno.keys())
    match_idx = X[:s2_rows, select_idx].argmax(axis=1)
    match_words = [idx_to_modelno[select_idx[match_idx[i,0]]] if match_idx[i,0] else np.nan for i in range(match_idx.shape[0])]
    r2.modelno.fillna(pd.Series(match_words, index=r2.index), inplace=True)
    
    
#     analagously filling r1s didn't improve    
    
    subset = ["modelno"]#, "brand"]
    # r1 can match to multiple r2s, but r2 matches only to 1 r1
    s1 = r1.rename(columns={"custom_id": "id1"}).dropna(subset=subset)
    s2 = r2.rename(columns={"custom_id": "id2"}).dropna(subset=subset)
    r3 = s1.merge(s2, on=subset).dropna(subset=["id1", "id2"])
    
    out = r3.merge(df_bag, how="outer", on="id2")
    out.loc[out.id1.isnull() & (out.score > 0.82 ), "id1"] = out.id1_bag 
    return out.dropna(subset=["id1"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory")
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()
    if args.train:
        train(args.input_directory)
    else:
        run(args.input_directory)



