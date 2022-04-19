import json

import pandas as pd

data = json.load(open("DATA/comments_3.json"))


comments = []
for row in data:
    try:
        if row['comment']:
            print(row['comment'])
            comments.append(row['comment'])
    except:
        pass
print(len(comments))
    # if 'comment_' in row
    # print(data[row])
comments = [item for sublist in comments for item in sublist]
data = pd.DataFrame(comments,columns=['comment'])
data = data.drop_duplicates(keep=False).reset_index(drop=True)
print(data.shape)
file_name = f"DATA/comments_3.csv"
data.to_csv(file_name, encoding='utf-8', index=False)
print(0)