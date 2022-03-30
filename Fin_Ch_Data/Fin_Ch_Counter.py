from asyncore import read
from collections import Counter
from itertools import count
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def read_data(path, unigram=True):
    with open(path, 'r', encoding='utf-8') as f:
        corpus = []
        for line in f:
            line = word_tokenize(line)
            #print(line)
            if unigram:
                for word in line:
                    word_lc = word.lower()
                    if word_lc not in string.punctuation and word not in stopwords.words('english'):
                        corpus.append(word_lc)
            else:
                for i in range(len(line)-1):
                    if  line[i].lower() not in string.punctuation and line[i].lower() not in stopwords.words('english'):
                        if line[i+1].lower() not in string.punctuation and line[i+1].lower() not in stopwords.words('english'):
                            word = line[i].lower() + " " + line[i+1].lower()
                            corpus.append(word)
    f.close()
    return corpus

def write_result(path, counter, freq=5):
    with open(path, 'w') as f:
        for item in counter:
            if item[1] >= freq:
                print(item, file=f)
    f.close()

def count_word(index, corpus):
    dict = {}
    for word in corpus:
        if word in index:
            if word in dict.keys():
                dict[word] += 1
            else:
                dict[word] = 1
    return dict
        
if __name__ == '__main__':
    read_paths = ['Finq1.txt', 'Finq2.txt', 'Finq3.txt', 'Chq1.txt', 'Chq2.txt', 'Chq3.txt']
    #read_paths = ['Chq3.txt']
    index_word_bi = ['critical thinking', 'self direction', 'self regulation', 'group work']
    index_word = ['creativity', 'communication', 'collaboration', 'technology', 'digital', 'self-direction', 'self-regulation', 'global', 'culture', 'local']
    fin_dict = {}
    ch_dict = {}
    for i in range(len(read_paths)):
        print('### Processing', read_paths[i])
        corpus_uni = read_data(read_paths[i])
        corpus_bi = read_data(read_paths[i], unigram=False)
        """
        Counting
        """
        if ('Fin' in read_paths[i]):
            fin_temp = count_word(index_word, corpus_uni)
            fin_temp_bi = count_word(index_word_bi, corpus_bi)
            fin_temp.update(fin_temp_bi)
            for key, value in fin_temp.items():
                if key in fin_dict.keys():
                    fin_dict[key] += value
                else:
                    fin_dict[key] = value
        else:
            ch_temp = count_word(index_word, corpus_uni)
            ch_temp_bi = count_word(index_word_bi, corpus_bi)
            ch_temp.update(ch_temp_bi)
            for key, value in ch_temp.items():
                if key in ch_dict.keys():
                    ch_dict[key] += value
                else:
                    ch_dict[key] = value
        """
        Unigram
        """
        counter_uni = Counter(corpus_uni)
        idx = read_paths[i].index('.')
        write_path = read_paths[i][:idx] + '_result' + read_paths[i][idx:]
        write_result(write_path, counter_uni.most_common(), freq=3)
        """
        Bigram
        """
        counter_bi = Counter(corpus_bi)
        idx = read_paths[i].index('.')
        write_path = read_paths[i][:idx] + '_result_bi' + read_paths[i][idx:]
        write_result(write_path, counter_bi.most_common(), freq=3)
    
    print('### Writing results')
    with open('Fin_count.txt', 'w') as f:
        for item in fin_dict.items():
            f.write(str(item) + '\n')
    f.close()
    with open('Ch_count.txt', 'w') as f:
        for item in ch_dict.items():
            f.write(str(item) + '\n')
    f.close()

