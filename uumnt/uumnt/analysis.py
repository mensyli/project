import os
import jieba
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from matplotlib.font_manager import FontProperties 


path = 'F:/Images/temp/uumnt/'
dirs = os.listdir(path)
if os.path.exists('filename.txt'):
    os.remove('filename.txt')
    
for dir in dirs:
    with open('filename.txt', 'a') as f:
        f.write(dir + '\n')

text = ''.join([line.replace('\n',' ') for line in set(open('filename.txt','rt').readlines())])
# jieba.load_userdict('jieba.txt')
segment_list = jieba.lcut(text, cut_all=False)

counter = {}
for segment in segment_list:
    counter[segment] = counter.get(segment,0) + 1

counter_sort = [x for x in sorted(counter.items(), key=lambda value: value[1],reverse=True) if x[0].strip() != ""]

if os.path.exists('words.json'):
    os.remove('words.json')
json = json.dumps(counter_sort,ensure_ascii=False)
with open('words.json','w+',encoding='utf-8') as f:
    f.write(json)

wordcloud = WordCloud(font_path='./msyh.ttc',max_words=100,height=600,width=1200).generate_from_frequencies(counter)

font = FontProperties(fname='./msyh.ttc', size=9)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
wordcloud.to_file('wordcloud.jpg')

ind = np.arange(len(counter_sort[:50]))
width = 0.5
fig, ax = plt.subplots()
rects = ax.bar(ind, tuple([x[1] for x in counter_sort][:50]), width)

ax.set_yticks([])
ax.set_xticks(ind)
ax.set_xticklabels(tuple([x[0] for x in counter_sort][:50]),fontproperties=font,rotation=90)
ax.legend(rects, 'm')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%int(height),
                ha='center', va='bottom')
autolabel(rects)
plt.show()