# NLTK SAMPLE CODES
from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

############################## SOUP
#2018 data
url = 'https://www.fantasypros.com/nfl/rankings/dynasty-rb.php'
response = get(url)
# print(response.text)

html_sp = BeautifulSoup(response.text, 'html.parser')
ranks = html_sp.find_all('input', class_ = 'wsis')
ranks_df = DataFrame( columns= 'data-id data-name data-team'.split())
for n in range(len(ranks)):
    ranks_df = ranks_df.append({'data-id': ranks[n]['data-id'],
                     'data-name': ranks[n]['data-name'],
                    'data-team': ranks[n]['data-team']}, ignore_index= True)

avgs = html_sp.find_all('td', class_= 'view-options ranks')
avgs_df = DataFrame([float(avgs[i].contents[0]) for i in range(len(avgs))]).values.reshape(-1, 4)
avgs_df = DataFrame(avgs_df, columns = 'Best Worst Average SD'.split())
final_df = pd.concat([ranks_df, avgs_df], axis= 1)

axes = sns.barplot(y= 'data-name', x= 'Average', data= final_df['data-name Average'.split()][:9], orient= 'h')


#2015 data
url_2015 = 'https://www.fantasypros.com/nfl/reports/leaders/rb.php?year=2015'
response_2015 = get(url_2015)
html_sp_2015 = BeautifulSoup(response_2015.text, 'html.parser')
avgs_2015 = html_sp_2015.find_all('td', class_= 'center')
names_2015 = html_sp_2015.find_all('a', class_= 'player-name')
temp = []
for i in avgs_2015:
    try:
        temp.append(float(i.text))
    except ValueError:
        temp.append(i.text)
names_temp = DataFrame([i.text for i in names_2015], columns= ['names'])
final_df = DataFrame(temp).values.reshape(-1,5)
final_df = DataFrame(final_df, columns= 'rank team points games average'.split())
final_df = pd.concat([names_temp, final_df], axis= 1)

axes_2015 = sns.barplot(y= 'names', x= 'average', data= final_df['names average'.split()][:10], orient= 'h')


############################## RE

import re

#1
string = "Earth is the third planet from the Sun"
result = re.findall(r'\b[A-Z|a-z]{2}', string)
print(result)

#2
string = 'abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz'
result = re.findall(r'@\w*.\w*', string)
print(result)

#3
string = 'Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009'
result = re.findall(r'\d{2}-\d{2}-\d{4}', string)
try:
    for i in pd.to_datetime(result).date:
        print(i)
except ValueError:
    print("This set of digits is not in time format")


#4
string = 'Earth\'s gravity interacts with other objects in space, especially the Sun and the Moon'
result = re.findall(r'\b[a|e|i|o|u]\w*', string, re.IGNORECASE)
print(result)

#5
lst = ['010-256-1354', '010-1234-5576', '070-642-0384', '010-290*-4858', '0105734123']

for i in lst:
    if re.findall(r'010-\d{3,4}-\d{4}', i):
        print("yes")
    else:
        print("no")


##############NLTK
import nltk
from nltk.corpus import gutenberg as gu
import random as rd
from sklearn.feature_extraction.text import CountVectorizer

def run(switch=True):
    if switch is True:
        print("you chose to filter stopwords")
    else:
        print("you chose not to filter stopwords")

    def find(lst2find, word_string, lst2add):
        # find the word(string) in the target list and return it in the storage list
        for i in lst2find:
            if word_string in i:
                lst2add.append(i)

    books_names = []
    for i in 'hamlet macbeth caesar paradise persuasion moby'.split():
        find(gu.fileids(), i, books_names)

    # functuation filtering
    def filter_puctuation(lst):
        punctuations = ['.', ',', '?', '!', '\'', '\"', ':', ';', '-', '[', ']', '(', ')', '{', '}', '."', '--', ',"']
        lst = [word for word in lst if word not in punctuations]
        return lst

    # stopword switch
    def filter_stopword(lst, switch_stopword=1):
        if switch_stopword == False:
            pass
        else:
            stopword_lst = nltk.corpus.stopwords.words(
                'english') + 'thou thy would shall could thy thee may must upon ye the might'.split()
            lst = [word.lower() for word in lst if word.lower() not in stopword_lst]
        return lst

    def filter_uselesswords(lst):
        uselesswords = 'ham'.split()
        lst = [word for word in lst if word not in uselesswords]
        return lst

    # segmentation
    def segment(lst, seg_unit=5000):
        dict_doc = {}
        n_seg = (len(lst) // seg_unit)
        for seg in range(n_seg):
            dict_doc[seg] = []
            for k in range(seg_unit):
                try:
                    dict_doc[seg].append(lst[k + seg * seg_unit])
                except:
                    break
        return dict_doc

    # doc term matrices by book
    def doc_term_mat(dict2find, vocab_lst):
        temp_lst = []
        for k in dict2find.keys():
            temp_lst.append(' '.join(dict2find[k]))
        vectorizer = CountVectorizer(vocabulary=vocab_lst)
        a = vectorizer.fit_transform(temp_lst).toarray()
        return DataFrame(a, columns=vocab_lst)

    # make a dictionary for books segmented by words
    books_words = {}
    switch_stopword = 1
    for i in books_names:
        print(i)
        books_words[i] = gu.words(i)
        if i == 'melville-moby_dick.txt':
            books_words[books_names[-1]] = [books_words[books_names[-1]][i] for i in
                                            rd.sample(range(len(books_words[books_names[-1]])),
                                                      80000)]  # mobydick 80,000 words
        print('original: ', len(books_words[i]))
        books_words[i] = segment(books_words[i])
        print("segment: ", len(books_words[i]))

    for i in books_names:
        for key in books_words[i].keys():
            books_words[i][key] = filter_puctuation(books_words[i][key])
            books_words[i][key] = filter_stopword(books_words[i][key], switch_stopword=switch)
            books_words[i][key] = filter_uselesswords(books_words[i][key])


    # gathering all the words in the books
    entire_words = []
    for key in books_words.keys():
        for _, i in books_words[key].items():
            entire_words += i

    # entire_words= filter_punctuation(entire_words)
    # entire_words= filter_stopword(entire_words)

    # find the top 50 most frequently used words
    entire_freq = nltk.FreqDist([word.lower() for word in entire_words])
    entire_freq_lst = sorted(list(zip(entire_freq.values(), entire_freq.keys())), reverse=True)
    top50_freq = entire_freq_lst[:50]
    top50_freq_wd = [word for _, word in top50_freq]

    #doc_term_mat creation
    doc_term_mat_dict = {}
    for key in books_words.keys():
        doc_term_mat_dict[key] = doc_term_mat(books_words[key], top50_freq_wd)
    # total by author
    # Shakespear
    temp = np.array([doc_term_mat_dict[books_names[0]][i].sum() + doc_term_mat_dict[books_names[1]][i].sum() +
                     doc_term_mat_dict[books_names[2]][i].sum()
                     for i in top50_freq_wd]).reshape(1, -1)
    freq_shakespear = DataFrame(temp, columns=top50_freq_wd)
    # Milton
    temp = np.array([doc_term_mat_dict[books_names[3]][i].sum() for i in top50_freq_wd]).reshape((1, -1))
    freq_milton = DataFrame(temp, columns=top50_freq_wd)
    # Austen
    temp = np.array([doc_term_mat_dict[books_names[4]][i].sum() for i in top50_freq_wd]).reshape((1, -1))
    freq_austen = DataFrame(temp, columns=top50_freq_wd)
    # Melville
    temp = np.array([doc_term_mat_dict[books_names[5]][i].sum() for i in top50_freq_wd]).reshape((1, -1))
    freq_melville = DataFrame(temp, columns=top50_freq_wd)
    freq_dict = {'Shakespeare': freq_shakespear, 'Milton': freq_milton,
                 'Austen': freq_austen, 'Melville': freq_melville}

    # draw the charts
    fig1, axes1 = plt.subplots()
    axes1.plot(freq_shakespear.columns, freq_shakespear.values[0], color='b')
    axes1.plot(freq_milton.columns, freq_milton.values[0], color='r')
    axes1.plot(freq_austen.columns, freq_austen.values[0], color='g')
    axes1.plot(freq_melville.columns, freq_melville.values[0], color='k')
    name = "stopwords filtering " + "%s"%switch + " Frequency"
    plt.title(name)
    plt.show()
    # sns.barplot(y= freq_melville.values[0], x= freq_melville.columns)

    # Frequency Matrix by Author
    author_dict = {}
    author_dict['Shakespeare'] = pd.concat(
        (doc_term_mat_dict[books_names[0]], doc_term_mat_dict[books_names[1]], doc_term_mat_dict[books_names[2]]),
        axis=0)
    author_dict['Milton'] = doc_term_mat_dict[books_names[3]]
    author_dict['Austen'] = doc_term_mat_dict[books_names[4]]
    author_dict['Melville'] = doc_term_mat_dict[books_names[5]]

    # Normalizing
    import copy

    author_norm_dict = copy.deepcopy(author_dict)
    for key in author_dict.keys():
        mean = author_dict[key].mean(axis=0)
        std = author_dict[key].std(axis=0)
        for col in author_dict[key].columns:
            if std[col] == 0:
                std[col] = 1
                print(col, " is counted 0. Thus, STD is adjusted to 1 for the sake of calculation")
            author_norm_dict[key][col] = (author_dict[key][col] - mean[col]) / std[col]

    # SVD_S
    colors_dict = {'Shakespeare': "#FFCCFF", 'Milton': '#CC99FF', 'Austen': '#E5FFCC', 'Melville': '#CCE5FF'}
    markers_dict = {'Shakespeare': "s", 'Milton': '2', 'Austen': 'o', 'Melville': '+'}

    fig2, axes2 = plt.subplots()
    for key in author_norm_dict.keys():
        s, _, _ = np.linalg.svd(author_norm_dict[key])
        axes2.scatter(s[:, 0], s[:, 1], label=key, marker=markers_dict[key], color=colors_dict[key])
    # plt.legend(loc= 'best')
    name = "stopwords filtering " + "%s" % switch + " SVD S"
    plt.title(name)
    plt.show()

    # SVD_D
    locs_fig = [221, 222, 223, 224]
    cmaps_dict = {'Shakespeare': "Blues", 'Milton': 'Greens', 'Austen': 'Reds', 'Melville': 'Greys'}
    fig3, axes3 = plt.subplots()
    name = "stopwords filtering " + "%s" % switch + " SVD D"
    plt.title(name)
    for num, key in enumerate(author_norm_dict.keys()):
        _, _, vh = np.linalg.svd(author_norm_dict[key])
        plt.subplot(locs_fig[num])
        plt.scatter(vh[:, 0], vh[:, 1], label=key, marker=markers_dict[key], color=colors_dict[key])
        for c, txt in enumerate(top50_freq_wd):
            axes3.annotate(txt, xy=(vh[:, 0][c], vh[:, 1][c]))
        plt.legend(loc='best')
    plt.show()


for i in [True, False]:
    if i is True:
        print("This time, without stopwords")
        run(switch=i)
    else:
        print("This time, with stopwords")
        run(switch= i)
