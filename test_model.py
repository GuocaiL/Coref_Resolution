import json
import os
from word_check import *

data_path = os.path.dirname(os.path.abspath(__file__))
#使用自己的模型处理文本并保存结果
def handle_data():
    with open(os.path.join(data_path, 'data', 'coref_data.json')) as f, \
            open(os.path.join(data_path, 'data', 'coref_data_model.json'), 'w+') as g:
        # print(f.read()[:10])
        model_list = []
        json_data = json.load(f)
        i = 0
        for s in json_data['data']:
            try:
                _, _ls, result = coref_no_zero(s['text'])
                model_list.append({'text':s['text'], 'coref': result})
                print(i, '---------------------------->',len(json_data['data']))
                # if i == 5:
                #     break
                # if i >= 1604:
                #     print(s['text'])
                #     _, _, result = coref_no_zero(s['text'])
                #     model_list.append({'text': s['text'], 'coref': result})

            except BaseException as e:
                print(i, "----------->出错")
                print(s['text'])
                print(e)
            finally:
                i += 1

        json.dump({"data":model_list}, g, ensure_ascii = False)

handle_data()