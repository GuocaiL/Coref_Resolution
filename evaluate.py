
def evaluation_LEA(key_list, response_list):
    '''
    :param key_list: 标注集的输入，格式为[{'text': 'XXX', 'name1': [xxx, xxx], 'name2': [xxx, xxx], ...}, ...]
    :param response_list: 系统预测集的输入，格式为[{'text': 'XXX', 'name1': [xxx, xxx], 'name2': [xxx, xxx], ...}, ...]
    :return: p，r，f1
    '''

    # 计算link数目
    def cal_link(n):
        return n * (n - 1) / 2

    # 格式化输入
    def format_input(input_list):
        format_list = []
        for d in input_list:
            for k, v in d.items():
                if k != 'text':
                    format_list.append(set(v).add(k))
        return format_list

    # 计算共指集合的元素总个数
    def sum_list(_list):
        sum_ = 0
        for x in _list:
            sum_ += len(x)
        return sum_

    #计算公式分子
    def mol(out_list, in_list):
        _mol = 0
        for n in out_list:
            cur_ = 0
            for m in in_list:
                cur_ += cal_link(len(m & n)) / cal_link(len(n))
            _mol += len(n) * cur_
        return _mol

    key_list = format_input(key_list)
    response_list = format_input(response_list)

    sum_key = sum_list(key_list)
    sum_res = sum_list(response_list)

    r_mol = mol(key_list, response_list)
    p_mol = mol(response_list, key_list)

    p = p_mol / sum_res
    r = r_mol / sum_key

    return p, r, 2 * p * r / (p + r)






