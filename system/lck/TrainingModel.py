import jieba
import numpy as np
import pandas as pd
from collections import namedtuple

class TrainingModel:
    # 将datafrem转换为list
    def myiter(self, d, cols=None):
        if cols is None:
            v = d.values.tolist()
            cols = d.columns.values.tolist()
        else:
            j = [d.columns.get_loc(c) for c in cols]
            v = d.values[:, j].tolist()

        n = namedtuple('MyTuple', cols)

        for line in iter(v):
            yield n(*line)

    #打开词典文件，返回列表
    def open_dict(Dict = 'data', path=r'./Textming/'):
        path = path + '%s.txt' % Dict
        dictionary = open(path, 'r', encoding='utf-8')
        dict = []
        for word in dictionary:
            word = word.strip('\n')
            dict.append(word)
        return dict

    def judgeodd(self, num):
        if (num % 2) == 0:
            return 'even'
        else:
            return 'odd'

    # 注意，这里你要修改path路径。
    deny_word = open_dict(Dict='否定词', path=r'./Textming/')
    posdict = open_dict(Dict='positive', path=r'./Textming/')
    negdict = open_dict(Dict='negative', path=r'./Textming/')

    degree_word = open_dict(Dict='程度级别词语', path=r'./Textming/')
    mostdict = degree_word[degree_word.index('extreme') + 1: degree_word.index('very')]  # 权重4，即在情感词前乘以4
    verydict = degree_word[degree_word.index('very') + 1: degree_word.index('more')]  # 权重3
    moredict = degree_word[degree_word.index('more') + 1: degree_word.index('ish')]  # 权重2
    ishdict = degree_word[degree_word.index('ish') + 1: degree_word.index('last')]  # 权重0.5

    def sentiment_score_list(self,dataset):
        seg_sentence = dataset.split('。')

        count1 = []
        count2 = []
        for sen in seg_sentence: #循环遍历每一个评论
            segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
            i = 0 #记录扫描到的词的位置
            a = 0 #记录情感词的位置
            poscount = 0 #积极词的第一次分值
            poscount2 = 0 #积极词反转后的分值
            poscount3 = 0 #积极词的最后分值（包括叹号的分值）
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in self.posdict:  # 判断词语是否是情感词
                    poscount += 1
                    c = 0
                    for w in segtmp[a:i]:  # 扫描情感词前的程度词
                        if w in self.mostdict:
                            poscount *= 4.0
                        elif w in self.verydict:
                            poscount *= 3.0
                        elif w in self.moredict:
                            poscount *= 2.0
                        elif w in self.ishdict:
                            poscount *= 0.5
                        elif w in self.deny_word:
                            c += 1
                    if self.judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i + 1  # 情感词的位置变化

                elif word in self.negdict:  # 消极情感的分析，与上面一致
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in self.mostdict:
                            negcount *= 4.0
                        elif w in self.verydict:
                            negcount *= 3.0
                        elif w in self.moredict:
                            negcount *= 2.0
                        elif w in self.ishdict:
                            negcount *= 0.5
                        elif w in self.degree_word:
                            d += 1
                    if self.judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1
                elif word == '！' or word == '!':  ##判断句子是否有感叹号
                    for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                        if w2 in self.posdict or self.negdict:
                            poscount3 += 2
                            negcount3 += 2
                            break
                i += 1  # 扫描词位置前移


                # 以下是防止出现负数的情况
                pos_count = 0
                neg_count = 0
                if poscount3 < 0 and negcount3 > 0:
                    neg_count += negcount3 - poscount3
                    pos_count = 0
                elif negcount3 < 0 and poscount3 > 0:
                    pos_count = poscount3 - negcount3
                    neg_count = 0
                elif poscount3 < 0 and negcount3 < 0:
                    neg_count = -poscount3
                    pos_count = -negcount3
                else:
                    pos_count = poscount3
                    neg_count = negcount3

                count1.append([pos_count, neg_count])
            count2.append(count1)
            count1 = []

        return count2

    def sentiment_score(self, senti_score_list):
        score = []
        for review in senti_score_list:
            score_array = np.array(review)
            Pos = np.sum(score_array[:, 0])  # 积极情感分数
            Neg = np.sum(score_array[:, 1])  # 消极情感分数
            AvgPos = np.mean(score_array[:, 0])  # 积极情感均值
            AvgPos = float('%.1f' % AvgPos)
            AvgNeg = np.mean(score_array[:, 1])  # 消极情感分值
            AvgNeg = float('%.1f' % AvgNeg)
            StdPos = np.std(score_array[:, 0])  # 积极情感方差
            StdPos = float('%.1f' % StdPos)
            StdNeg = np.std(score_array[:, 1])  # 消极情感方差
            StdNeg = float('%.1f' % StdNeg)
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        return score

    def __init__(self):

        # 加载获取到的用户信息
        df1 = pd.read_csv('./system/lck/Users.csv', index_col=None)
        data_message = pd.DataFrame(df1)
        data_list = list(self.myiter(data_message))

        Data_list = []
        for cell_message in data_list:
            data_list1 = []
            data_list1.append(cell_message[0])
            data_list1.append(cell_message[1])
            data_list1.append(cell_message[2])
            data_list1.append(cell_message[3])
            data_list1.append(cell_message[4])
            data_list1.append(cell_message[5])
            cell_message = str(cell_message[6])
            Score = self.sentiment_score(self.sentiment_score_list(cell_message))
            data_list1.append(cell_message)
            for cell in Score[0]:
                data_list1.append(cell)
            print(data_list1)
            Data_list.append(data_list1)

        df_Sheet1 = pd.DataFrame(Data_list, columns=['用户id', '用户姓名', '发表日期', '国家', '省份', '市区', '说说内容',
                                                     '积极情感分数', '消极情感分数', '积极情感均值', '消极情感均值', '积极情感方差',
                                                     '消极情感方差'])
        df_Sheet1.to_csv('./Score.csv')

# model = TrainingModel()