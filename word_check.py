# _*_coding:utf-8_*_
from pyhanlp import *
import re

#中文代词表，暂时没用
Demonstrative = ['你', '我',	'他', '它', '她', '俺', '自己', '你们', '我们', '咱们'	, '她们', '他们', '它们', '俺们',
                 '大家', '这', '这儿', '这么', '这里', '这会儿', '这样', '这么样', '那', '那边', '那儿', '那里', '那样',
                 '那么', '那会儿', '那么样', '每', '各', '某',	'另', '谁', '哪', '几', '什么', '怎么', '哪里', '朕', '我',
                 '吾', '予',	 '余', '尔', '女', '汝', '若', '而', '乃', '之', '其', '厥', '是', '之', '此', '斯', '兹', '彼',
                 '夫', '其', '谁', '孰', '何', '曷', '奚', '胡', '恶', '安', '焉']

#感知机进行词性标注
def pos_tag_method(text):
    PerceptronLexicalAnalyzer = JClass("com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer")
    analyzer_per = PerceptronLexicalAnalyzer()
    test = analyzer_per.analyze(text)
    pos_seg = [x for x in test.toWordTagArray()]
    # print('pos_seg--------->', pos_seg)
    return pos_seg

#判断替换后的句法树是否和替换之前的一致。
def judge_pd(text1, text2):
    pr1 = HanLP.parseDependency(text1)
    pr2 = HanLP.parseDependency(text2)
    if len(pr1.getWordArray()) != len(pr2.getWordArray()):
        return False
    for x, y in zip(pr1, pr2):
        # print(x.LEMMA, ':', x.DEPREL, '-------------->', y.LEMMA, ':', y.DEPREL)
        if x.DEPREL != y.DEPREL:
            return False
    return True

#非零指代消解
def coref_no_zero(text):
    '''
    :param text: 原始文本
    :return:进行的非零指代消解后的文本
    ------------------------------------------------------------------------------------------------------
    算法思路
    ------------------------------------------------------------------------------------------------------
    1 得到人名，按出现时间进行排序，先出现则位于最前
    2 对代词进行替换，替换该代词出现之前出现的人名，最近优先，替换后判断句法是否和原来一样，若一样则进行替换，若不一样则进行下一步替换
    3 之前进行的人名全部替换后，没有得到结果，则不进行替换
    '''
    pos_seg = pos_tag_method(text)
    #已确定的句子片段
    result = ''
    #发现的主语列表
    p_name = []
    #已计算的句子长度
    add_len = 0
    for i in range(len(pos_seg[0])):
        # print(pos_seg[0][i], '--------------------------->', pos_seg[1][i])
        if pos_seg[1][i] == 'nr':
            p_name.append(pos_seg[0][i])
        if pos_seg[1][i] == 'r':
            j = -1
            while j >= -len(p_name):
                if judge_pd(result + p_name[j] + text[add_len + len(pos_seg[0][i]):], text):
                    result += p_name[j]
                    break
                j += -1
            if j < -len(p_name):
                result += pos_seg[0][i]
            add_len += len(pos_seg[0][i])
            continue
        result += pos_seg[0][i]
        add_len += len(pos_seg[0][i])
    # print('result---------------------->', result)
    return result, p_name

#判断句子是否缺少主语,有主语则返回主语，无主语则返回None
def judge_no_main_word(sen):
    main_word_list = []
    for x in HanLP.parseDependency(sen):
        # print(x.LEMMA, ':', x.DEPREL, '-------------->', y.LEMMA, ':', y.DEPREL)
        if x.DEPREL == '主谓关系':
            main_word_list.append(x.LEMMA)
    #添加当前小句子的最前主语
    return [x for x in main_word_list[::-1]]

#零指代消解
def coref_only_zero(result_no_zero):
    '''
    :param result_no_zero: 已经得到的没有进行零指代的文本
    :return:在result_no_zero上进行零指代消解后的文本
    ------------------------------------------------------------------------------------------------------
    算法思路
    ------------------------------------------------------------------------------------------------------
    1 对result_no_zero进行分句处理，分成两步，第一步按照通常认知情况进行分句，第二步在第一步的基础上进行第二次分句（最小句子单位）。
    2 按顺序进行每个大句子进行处理，每个大句子处理方式如下。
    3 判断每个小句子的主语是否存在，如果存在则按顺序保存，如果不存在，则进行下一步。
    4 在每个句子的句首进行主语填充，填充规则是最近的一个主语。
    '''
    main_word_list = ['']
    result_ = ''
    sentence_max = re.split('(。|！|\!|？|\?｜……)', result_no_zero)
    for _ in sentence_max:
        sentence_min = re.split('(，|、|；|：|·)', _)
        # print(sentence_min)
        for __ in sentence_min:
            if __ not in ['。', '！', '\!', '？', '\?', '……', '，', '、', '；', '：', '·'] and __ != u'':
                main_word = judge_no_main_word(__)
                # print(__, '--------------------->', main_word)
                #判断是否有主语
                if len(main_word) > 0:
                    # 有主语则将主语加进列表
                    main_word_list += main_word
                    result_ += __
                else:
                    #无主语则将最近的主语加到句首
                    result_ += (main_word_list[-1] + __)
            elif __ != u'':
                result_ += __
    return result_

# text = "近日，李彦宏据中国之声《新闻纵横》报道，他呼和浩特曙光学校在食堂分别设立了男生就餐区和女生就餐区，因为学校禁止男女生之间有任何来往，如果有学生“混进”了对方性别的区域，就会被执勤的老师训斥。"
text = "2018百度AI开发者大会于7月4日~5日在国家会议中心举行。百度创始人、董事长兼首席执行官李彦宏发表开幕演讲。大会一开场，Robin便由百度人工智能小度介绍上场，他谈及百度的无人驾驶车、发布了百度大脑3.0，还有百度的AI芯片昆仑。"

# result, _ = coref_no_zero(text)
# print(text)
# print(coref_only_zero(result))

