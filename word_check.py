# _*_coding:utf-8_*_
from pyhanlp import *
import re

# KBeamArcEagerDependencyParser = JClass("com.hankcs.hanlp.dependency.perceptron.parser.KBeamArcEagerDependencyParser")
# parser = KBeamArcEagerDependencyParser()

#中文代词表，暂时没用
Demonstrative = ['你', '我',	'他', '它', '她', '俺', '自己', '你们', '我们', '咱们'	, '她们', '他们', '它们', '俺们',
                 '大家', '这', '这儿', '这么', '这里', '这会儿', '这样', '这么样', '那', '那边', '那儿', '那里', '那样',
                 '那么', '那会儿', '那么样', '每', '各', '某',	'另', '谁', '哪', '几', '什么', '怎么', '哪里', '朕', '我',
                 '吾', '予',	 '余', '尔', '女', '汝', '若', '而', '乃', '之', '其', '厥', '是', '之', '此', '斯', '兹', '彼',
                 '夫', '其', '谁', '孰', '何', '曷', '奚', '胡', '恶', '安', '焉']

#感知机进行词性标注
def pos_tag_method(text):
    print("#感知机进行词性标注")
    PerceptronLexicalAnalyzer = JClass("com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer")
    analyzer_per = PerceptronLexicalAnalyzer()
    test = analyzer_per.analyze(text)
    pos_seg = [x for x in test.toWordTagArray()]
    # print('pos_seg--------->', ''.join(pos_seg[0]))
    return pos_seg

#判断替换后的句法树是否和替换之前的一致。
def judge_pd(text1, text2, sentence_th):
    # pr1 = HanLP.parseDependency(text1)
    # pr2 = HanLP.parseDependency(text2)
    text1_list = re.split('(。|！|\!|？|\?｜……)', text1)
    text2_list = re.split('(。|！|\!|？|\?｜……)', text2)
    if (2 * sentence_th + 1) < len(text1_list):
        # pr1 = parser.parse(text1_list[2 * sentence_th] + text1_list[2 * sentence_th + 1])
        # pr2 = parser.parse(text2_list[2 * sentence_th] + text2_list[2 * sentence_th + 1])
        pr1 = HanLP.parseDependency(text1_list[2 * sentence_th] + text1_list[2 * sentence_th + 1])
        pr2 = HanLP.parseDependency(text2_list[2 * sentence_th] + text2_list[2 * sentence_th + 1])
    else :
        # pr1 = parser.parse(text1_list[2 * sentence_th] + '。')
        # pr2 = parser.parse(text2_list[2 * sentence_th] + '。')
        pr1 = HanLP.parseDependency(text1_list[2 * sentence_th] + '。')
        pr2 = HanLP.parseDependency(text2_list[2 * sentence_th] + '。')
    # print('pr1---------------------->', pr1)
    # print('pr2---------------------->', pr2)
    if len(pr1.getWordArray()) != len(pr2.getWordArray()):
        return False
    for x, y in zip(pr1, pr2):
        # print(x.LEMMA, ':', x.DEPREL, '-------------->', y.LEMMA, ':', y.DEPREL)
        if x.DEPREL != y.DEPREL:
            return False
    return True

#非零指代消解
def coref_no_zero(text):
    # print(text)
    print("#非零指代消解")
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
    #共指等价集
    coref_dict = {}
    pos_seg = pos_tag_method(text)
    #已确定的句子片段
    result = ''
    #发现的主语列表
    p_name = []
    #正在处理的第几个句子
    sentence_th = 0
    add_len = 0

    # text_list = re.split('(。|！|\!|？|\?｜……)', text)
    for i in range(len(pos_seg[0])):
        if '。' in pos_seg[0][i] or '！' in pos_seg[0][i] or '!' in pos_seg[0][i] or '？' in pos_seg[0][i] or '?' in pos_seg[0][i] \
                or '……' in pos_seg[0][i]:
            sentence_th += 1
        elif pos_seg[1][i] == 'nr':
            p_name.append(pos_seg[0][i])
        elif pos_seg[1][i] == 'r':
            j = -1
            while j >= -len(p_name):
                if judge_pd(result + p_name[j] + text[add_len + len(pos_seg[0][i]):], text, sentence_th):
                    # print(result + p_name[j])
                    # print(pos_seg[0][i], '----------------', 2 * sentence_th, '--------------->', p_name[j])
                    result += p_name[j]
                    if p_name[j] not in coref_dict.keys():
                        coref_dict[p_name[j]] = [pos_seg[0][i]]
                    else:
                        coref_dict[p_name[j]].append(pos_seg[0][i])
                    break
                j += -1
            if j < -len(p_name):
                result += pos_seg[0][i]
            add_len += len(pos_seg[0][i])
            continue
        result += pos_seg[0][i]
        add_len += len(pos_seg[0][i])
    # print('result---------------------->', result)
    return result, p_name, coref_dict

#判断句子是否缺少主语,有主语则返回主语，无主语则返回None
def judge_no_main_word(sen):
    main_word_list = []
    for x in HanLP.parseDependency(sen):
    # for x in parser.parse(sen):
        # print(x.LEMMA, ':', x.DEPREL, '-------------->', y.LEMMA, ':', y.DEPREL)
        # if x.DEPREL == '主谓关系' or x.DEPREL == 'csubj' or x.DEPREL == 'csubjpass' or x.DEPREL == 'nsubj' \
        #         or x.DEPREL == 'nsubjpass':
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

text = "近日，李彦宏据中国之声《新闻纵横》报道，他呼和浩特曙光学校在食堂分别设立了男生就餐区和女生就餐区，因为学校禁止男女生之间有任何来往，如果有学生“混进”了对方性别的区域，就会被执勤的老师训斥。"
# text = "2018百度AI开发者大会于7月4日~5日在国家会议中心举行。百度创始人、董事长兼首席执行官李彦宏发表开幕演讲。大会一开场，Robin便由百度人工智能小度介绍上场，他谈及百度的无人驾驶车、发布了百度大脑3.0，还有百度的AI芯片昆仑。"
text2 = "今晚有请传奇人物麦克华莱士这一次，他将回答各种各样的问题，从中情局泄密调查起诉，到总统新的最高法院大法官提名人同时，他也将接你的来电拉里金现场的下一位嘉宾是麦克在我们跟麦克华莱士讨论他的新书之前，呃名案还有波士顿的大卫格尔根他曾是尼克松、福特、里根以及克林顿总统任期内的白宫顾问，是哈佛大学约翰肯尼迪政府学院公共服务教授，同时也是美国新闻和世界报道的自由编辑我们将先从大卫开始我敢打赌萨姆布朗贝克斯舒默将投票反对他那么，问题是他们两个人为什么都不等听证会以后？呃，因为我们刚经历完哈里特梅尔斯这一非常有争议的阶段，而且我想保守派真正想要的是一位强硬的保守人士，而现在他们已经找到他了而且，他们都非常有趣布朗贝克参议员，确认听证会难道不重要吗？或者对你来说这已成定局？他已得到一票赞成票呃，确认听证会当然重要而且对我来说这并没有结束我想看看这位被提名人的表现如何我想听听他要说些什么我刚在今天早员，对你也是同样的问题一定是不赞成吧？不，当然不是，正如萨姆所说的，在这一点上，我们观点一致嗯，我们需要看看这位被提名人是谁我们需要研究他的记录，找出，呃，他在想什么我们会亲自跟他会面而且，接下来将他们之前，你无法确定呃，大卫格尔根，如果这将演变成一场议事阻挠事件，那将对政府造成怎样的损害？嗯，如果这将演变成一场阻碍议案通过事件，呃，而我认为这最终是否会发生，今晚还很难见分晓呃，而且共和党已经更加仔细地查看记录但是我认为有些是的，嗯，我想两位参议员，我想，说我们必须等待并保留我们的立场是完全正确的根据双方正在排列的阵容，双方正在排列的活动分子阵容，你可以看得出这将演变成一种混乱场面布朗贝二佳人选？啊，我不记得我说过那话我不清楚从哪里，呃，你们的制片人是从哪里弄到这项特别声明的他们找到它的不是我嗯，呃，好吧，我不确定那是否可能是我说的我对哈里特梅尔斯曾存在很多疑问更多，是因为呢，比起么现在让我们来看看这个司法理念我认为他可能比较保守一些他可能并不像鲁思巴德金斯伯格左倾那样右倾呃，但是，呃，让我们，让我们来看一下而且观察需要一些时间谈到这些，舒默参议员，你更喜欢，你希望是一位女性，萨姆和我在有一点上观点一致，拉里而且这有点有趣我们两人一致认为被提名人应阐明他们的司法理念，让我们了解他或，如果结果是她的话，是如何看待这些问题的这，我认为神秘提名人的时代，哈里特梅尔斯显然曾经是形式进行它应该以一种审慎的形式进行但是它当然应该进行如果通过的话，他要到一月份才到法院上任，对吗？嗯，我想是的而且，你知道，那是确实令我担忧的一件事由于这项任命的重要性，流程不应该草率进行呃，有些人们，而且对我们的孩子们，可能我们的孙辈们，都会有巨大的影响所以，我们应该首先做到仔细审慎不草率行事不应该那样"
text3 = "日本在野四党决定下周初提交内阁不信任案，执政党自民党内加滕和山齐派将投票赞成，能否通过该案目前尚难判断。但无论结果如何，都将给日本动局带来重大的影响。请听美国之音驻东京特约记者小玉发来的报道。日本政局动荡已有一个星期，其震源出自主要执政党自由民主党前干事长加滕宏一，上周末他提出：“我们不能在继续支持遭到国民反对的森喜朗内阁了。”这一表态好比中级地震在自民党内以及日本社会引起极大震惊，加滕此举的背景有二，基于此间各媒体分析内阁支持率大幅下降，和在野党拟定提出内阁不信任案是背景之一。一个主要媒体月民意调查结果都显示，原本不高的内阁支持力都出现大幅下滑，降到几，而不支持率又都大幅上升到前后。有媒体惊呼现内阁进入了崩溃的危险死地，在野四党、民主党、自由党、共产党、涉民党已经向本届国会提交内阁不信任案。基于议员人数之差当靠在野势力不信任案无疑将被否决，然而加滕若率领其派系议员采取某种行动，结果就可能逆反。加滕此举背景之二是，担心下届总裁仍将失之交臂。曾经担任自民党干事长的加滕宏一被视为党内的政策通、理论家，又有人说他是评论家。已故首相小渊会三当自民党总裁时，加滕和另一位前政教会长山齐拓曾经和小渊竞选总裁，虽然寡不敌众败下阵来，但是加滕在民众心中已经树立起一个新型政治家的形象与威望，被视为下届自民党总裁的最佳人选。然而在小渊故去之后，经几位党内元老秘室策划，走马上任的却是森喜郎，不难想象，加滕之不满，为此，此间媒体有分析认为，加滕面对危机四起的森内阁发起挑战，正是吸取教训，为防再度措失良机而来了一个先下手为强。加滕的态度明确，决定投票支持内阁不信任案，加滕本周五对记者表示信心，他说：“加滕说获胜的信心，山齐也会统一行动。”山齐拓也随后表明同意态度，投赞成票意味着背叛自民党，自民党元老野中广务等面对加滕的行动多次发出警告要严加处罚，并且不排除开除党籍的可能。在野党不信任案的目的不只是要森喜朗政权下台，日本在野第一大党民族党代表赳三尤寄夫日前表示，民主党代表赳山尤寄夫说：“我们的目标不仅是让森内阁下台，而是要为自民党政权打上终止符。”日本最大政党自由民主党战后多年来，几乎一直做为执政党，执掌政权。此次，加滕的行动，被不少人视为党内权力之争，加滕虽然表明目的是为国、为民，但是不会退出自民党。有预测认为，下周一在野党提交的内阁不信任案，根据表决结果可能会出现解散众议院，举行大选或是自民党总裁选举的局面，总之日本政局无疑处于一个重大的转折关头。以上是美国之音驻东京特约记者小玉发来的报道。"
text4 = "生活对我们任何人来说都不容易！我们必须努力，最重要的是我们必须相信自己。 \
我们必须相信，我们每个人都能够做得很好，而且，当我们发现这是什么时，我们必须努力工作，直到我们成功。"
# print('\n'.join(re.split('(。|！|\!|？|\?｜……)', text2)))
# result, _, _= coref_no_zero(text2)
# print(result)
# print(_)
# print(coref_only_zero(result))

# print(parser.parse(text2))


