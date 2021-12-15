# create by DavidChang
# create date 2021/12/15

import pandas as pd
import random

df = pd.read_csv(r"D:\99. python\yusun_contest\data\tbrain_cc_training_48tags_hash_final.csv", usecols=['chid','shop_tag','txn_amt'])
cate = ['2','6','10','12','13','15','18','19','21','22','25','26','36','37','39','48']
df = df[df.shop_tag.isin(cate)]
df = df.groupby(['chid','shop_tag'], as_index=False).sum('txn_amt')
df['rn'] = df.sort_values(['chid','txn_amt'], ascending = [True, False]).groupby('chid').cumcount() + 1
df = df[df.rn <= 3]
df = df.pivot(index = 'chid', columns = 'rn', values = 'shop_tag')
df = df.reset_index()
df.columns = ['chid', 'top1', 'top2', 'top3']

for i in range(len(df)):
    for j in range(1,4):
        if pd.isna(df.iloc[i,j]):
            df.iloc[i,j] = random.choice(list(set(cate) - set(df.iloc[i,1:4].tolist())))
