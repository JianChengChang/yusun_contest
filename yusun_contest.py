# create by DavidChang
# create date 2021/12/15


import numpy as np
import pandas as pd
import random
from numpy import int64
from tqdm import tqdm

df = pd.read_csv(r"D:\99. python\yusun_contest\data\tbrain_cc_training_48tags_hash_final.csv", usecols=['chid','shop_tag','txn_amt'])
cate = ['2','6','10','12','13','15','18','19','21','22','25','26','36','37','39','48']
df = df.groupby(['chid','shop_tag'], as_index=False).sum('txn_amt')
df['rn'] = df.sort_values(['chid','txn_amt'], ascending = [True, False]).groupby('chid').cumcount() + 1
df = df[df.rn <= 3]
df = df.pivot(index = 'chid', columns = 'rn', values = 'shop_tag')
df = df.reset_index()
df.columns = ['chid', 'top1', 'top2', 'top3']

for i in tqdm(range(len(df))):
    for j in range(1,4):
        if df.iloc[i,j] not in cate:
            if j == 1:
                if df.iloc[i,2] in cate:
                    df.iloc[i,1] = df.iloc[i,2]
                    df.iloc[i,2] = df.iloc[i,3]
                    df.iloc[i,3] = np.nan
                elif df.iloc[i,3] in cate:
                    df.iloc[i,1] = df.iloc[i,3]
                    df.iloc[i,3] = np.nan       
                else:
                    df.iloc[i,1] = np.nan

            elif j == 2:    
                if df.iloc[i,3] in cate:
                    df.iloc[i,2] = dfs.iloc[i,3]
                    df.iloc[i,3] = np.nan
                else:
                    df.iloc[i,2] = np.nan
            
            else:
                df.iloc[i,3] = np.nan

        if pd.isna(df.iloc[i,j]):
            df.iloc[i,j] = random.choice(list(set(cate) - set(df.iloc[i,1:4].tolist())))

df.top1 = df.top1.astype(int64)
df.top2 = df.top2.astype(int64)
df.top3 = df.top3.astype(int64)

df.to_csv(r"D:\99. python\yusun_contest\submission.csv", index = False)


dff = pd.read_csv(r"D:\99. python\yusun_contest\data\testdata.csv")