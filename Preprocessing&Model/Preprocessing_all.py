import json
import os
import sys
import re

reload(sys)

sys.setdefaultencoding('utf-8')

#---------------------------------------Preprocess for Yummy 66k--------------------------------------------------------

quantity_words = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
path = '.\yummy-66k'
file_path = []
res = []
id = 0
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file_path.append(os.path.join(root, name))
for cus_file in file_path:
    data = json.load(open(cus_file))
    for row in data:
        dic = {}
        dic["cuisine"] = row['cuisine'].lower()
        dic["id"] = id
        temp = []
        for item in row['ingredients']:
            content = item.split(',')[0].split(' ')
            j = 0
            for i in range(len(content)):
                try:
                    if content[i][0] in quantity_words:
                        j = i + 2
                except:
                    continue
            if len(content[j:]) != 0:
                temp.append(" ".join(content[j:]))
        dic["ingredients"] = [item.lower() for item in temp]
        id += 1
        res.append(dic)
    # print json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
    print 'OK'
with open('66K.json', 'w') as file:
    file.writelines(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))

# --------------------------------------Preprocess for Yummy 27k--------------------------------------------------------

quantity_words = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
cuisine = ['chinese', 'french', 'greek', 'indian', 'italian', 'japanese', 'mexican', 'spanish', 'thai',
           'irish', 'southern_us', 'korean', 'vietnamese', 'moroccan', 'cajun_creole', 'british', 'jamaican',
           'russian','filipino', 'brazilian']
path = '.\metadata27638'
file_path = []
res = []
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file_path.append(os.path.join(root, name))
for cus_file in file_path:
    row = json.load(open(cus_file))
    dic = {}
    # for row in data:
    if row['attributes']['cuisine'][0].lower() not in cuisine:
        continue
    cus = row['attributes']['cuisine'][0]
    dic["cuisine"] = cus.lower()
    temp = []
    for item in row['ingredientLines']:
        content = item.split(',')[0].split(' ')
        j = 0
        for i in range(len(content)):
            try:
                if content[i][0] in quantity_words:
                    j = i + 2
            except:
                continue
        if len(content[j:]) != 0:
            temp.append(" ".join(content[j:]))
    dic["ingredients"] = [item.lower() for item in temp]
    res.append(dic)
    print 'OK'
with open('27K.json', 'w') as file:
    file.writelines(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))

# -------------------------------------------Merge data together--------------------------------------------------------

path = '.\data'
file_path = []
res = []
id = 0
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file_path.append(os.path.join(root, name))
for cus_file in file_path:
    data = json.load(open(cus_file))
    for row in data:
        dic = {}
        dic["cuisine"] = row['cuisine'].lower()
        dic["id"] = id
        dic["ingredients"] = [item for item in row['ingredients']]
        id += 1
        res.append(dic)
    print 'OK'
with open('merge json.json', 'w') as file:
    file.writelines(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))

# -----------------------------------Preprocess to remove unuserful words-----------------------------------------------

data = json.load(open('merge json.json'))

for items in data:
    for ing in items['ingredients']:
        ing = re.sub(r'\(.*\)?', "", ing)
        ing = re.sub(r'\sand\s', "", ing)
        ing = re.sub(r'\sor\s', "", ing)
        ing = re.sub(r'\stsp\s', "", ing)
        ing = re.sub(r'oz\.\)', "", ing)
        ing = re.sub(r'ounce/..*\)', "", ing)
        ing = re.sub(r'\stbsp\s', "", ing)
        ing = re.sub(r'\d', "", ing)
        ing = re.sub(r'\w', "", ing)
        ing = re.sub(r'\(*', "", ing)
    temp = []
    for ing in items['ingredients']:
        if len(ing) != 0:
            temp.append(ing)
    items['ingredients'] = temp

with open('merge_f1.json', 'w') as file:
    file.writelines(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

# -----------------------------------Turn normal json format into pyspark json------------------------------------------

from sklearn.model_selection import train_test_split
res = []
train = []
test = []
dic = {}
lab = 0
train_data = json.load(open('./merge_f1.json'))
for row in train_data:
    temp = "{"
    if row['cuisine'] not in dic:
        dic[row['cuisine']] = lab
        lab += 1
    temp += "\"label\": " + str(dic[row['cuisine']]) + ",\"cuisine\": \"" \
    + row['cuisine'] + "\",\"id\": " + str(row['id']) + ",\"ingredients\": "
    ingre = ",".join(row['ingredients']).lower().replace(" ","-")
    temp += "\"" + ingre + "\"}\n"
    res.append(temp)
train, test = train_test_split(res, test_size=0.25, random_state=34)
with open('./train.json', 'w') as file:
    for item in res:
        file.writelines(item)
with open('./test.json', 'w') as file:
    for item in test:
        file.writelines(item)