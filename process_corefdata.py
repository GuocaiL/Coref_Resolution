import xmltodict
import json
import re
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#保留中文信息
def leave_chinese(str_list):
    out_list = []
    for s in str_list:
        # 匹配不是中文、标点符号的其他字符
        cop = re.compile(
            "[^\u4e00-\u9fa5&\u3002&\uff1f&\uff01&\uff0c&\u3001&\uff1b&\uff1a&\u201c&\u201d&\u2018&\u2019&\uff08&"
            "\uff09&\u300a&\u300b&\u3008&\u3009&\u3010&\u3011&\u300e&\u300f&\u300c&\u300d&\ufe43&\ufe44&\u3014"
            "&\u3015&\u2026&\u2014&\uff5e&\ufe4f&\uffe5]")
        # 将string1中匹配到的字符替换成空字符
        out_list.append(cop.sub('', s))
    return out_list

#json版算法，文本格式为xml，故废弃
def add_coref(d, _dict):
    print(_dict)
    if "COREF" not in d:
        if str(d["@ID"]) not in _dict.keys():
            _dict[d["@ID"]] = [''.join(leave_chinese(d["#text"]))]
        else :
            _dict[d["@ID"]].append(''.join(leave_chinese(d["#text"])))
        return d["#text"]
    else :
        ss = add_coref(d["COREF"], _dict)
        if d["@ID"] not in _dict.keys():
            _dict[d["@ID"]] = [''.join(leave_chinese(d["#text"] + ss))]
        else :
            _dict[d["@ID"]].append(''.join(leave_chinese(d["#text"]) + ss))
        return d["#text"] + ss
#json版算法，文本格式为xml，故废弃
def format_coref(coref_dict_list):
    _dict = {}
    for d in coref_dict_list:
        add_coref(d, _dict)
    return _dict

# XML版算法
def format_coref_my_deep(elem, text_coref, tag_first = True):
    if elem.tag == "DOC":
        # print("DOC.child--------------------->", elem.getchildren())
        for item_doc in elem.getchildren():
            text_coref.append({})
            format_coref_my_deep(item_doc, text_coref)
    elif elem.tag == "TEXT":
        # print("TEXT.child--------------------->", elem.getchildren())
        for elem_text in elem.getchildren():
            format_coref_my_deep(elem_text, text_coref)
    elif len(elem.getchildren()) == 0 and elem.tag == "COREF":
        if elem.attrib['ID'] not in text_coref[-1].keys():
            text_coref[-1][elem.attrib['ID']] = [''.join(leave_chinese(str(elem.text)))]
        else:
            text_coref[-1][elem.attrib['ID']].append(''.join(leave_chinese(str(elem.text))))
        if tag_first:
            return str(elem.text)
        else:
            return str(elem.text + str(elem.tail))
    elif len(elem.getchildren()) > 0 and elem.tag == "COREF":
        coref_str = ''
        for elem_coref in elem.getchildren():
            coref_str = format_coref_my_deep(elem_coref, text_coref, False)
        if not tag_first:
            coref_str += str(elem.text)
        if elem.attrib['ID'] not in text_coref[-1].keys():
            text_coref[-1][elem.attrib['ID']] = [''.join(leave_chinese(str(elem.text) + coref_str))]
        else:
            text_coref[-1][elem.attrib['ID']].append(''.join(leave_chinese(str(elem.text) + coref_str)))
        return str(coref_str)

with open('./data/coref_data.json', 'w+', encoding='utf-8') as g:
    for fpathe,dirs,fs in os.walk('./data/annotations'):
      for file in fs:
          if file.endswith('.coref'):
            with open(os.path.join(fpathe,file)) as f:
                print(os.path.join(fpathe,file))
                tree = ET.ElementTree(file=os.path.join(fpathe,file))
                root = tree.getroot()
                data = f.read()
                text_list = leave_chinese(data.split("</TEXT>"))
                # di = xmltodict.parse(data)
                # da = json.dumps(di)
                # d = json.loads(da)
                text_coref = []
                format_coref_my_deep(root, text_coref)
                for text, coref in zip(text_list, text_coref):
                    # print(text)
                    # print(coref)
                    json.dump({'text':text, 'coref': coref}, g, ensure_ascii=False)






