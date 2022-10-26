#!/usr/bin/env python3
import pickle
import json
import jieba
import os
import argparse

database = 'input_method.pickle'


def isChinese(string):
    """
    判断一段字符串是否全为汉字
    """
    for char in string:
        if not (0x4e00<=ord(char)<0x9fa5):
            return False
    
    return True


def train_input_method(text: str, stats: dict = {}):
    """
    更新输入法字典stats, stats中既包含单字联想候选字也包含词语联想候选字
    """
    # 更新单字联想字频
    for i in range(len(text) - 1):
        this = text[i]
        nextChar = text[i + 1]
        if not isChinese(this):
            continue
        elif this not in stats:
            stats[this] = {}
        if isChinese(nextChar):
            stats[this][nextChar] = stats[this].get(nextChar, 0) + 1
    
    # 更新词语联想字频
    words = jieba.lcut(text, cut_all=False)  # 精准模式
    for i in range(len(words) - 1):
        word = words[i]
        nextChar = words[i + 1][0]
        if isChinese(word) and len(word)>1:  # 要求word是二字及以上词语且全为汉字
            if word not in stats:
                stats[word] = {}
            if isChinese(nextChar):  # 若下一个字也是汉字则计入统计
                stats[word][nextChar] = stats[word].get(nextChar, 0) + 1
    return stats


def input_method(query: str, stats: dict, n: int = 50):
    """
    输入法字典stats中既包含单字联想数据也包含词语联想数据, 输入字或词即可查询候选字(按候选字频排序)
    """
    if len(query)>1:
        if query in stats:
            print(query, "是词语")
        else:
            print(query, "不是词语")
            return

    if query not in stats and len(query)==1:
        print(query, '超出联想输入法范围')
        return

    print(f"其后高频字为(依字频排序, 最多{n}字)")
    for i in range(len(stats[query])):
        if i > n - 1:
            break
        print(f'{stats[query][i]}', end='\t')
        if i % 10==9:
            print()
    return stats[query]


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='The maximum number of candidates', type=int, default=50)
    args = parser.parse_args()
    return args


def main(file: str):
    """
    file代表用于训练输入法的文件路径, 训练完成后把输入法数据存入database并利用其进行联想输入, 输入esc终止
    """
    args = parse()
    if not os.path.exists(database):
        print("不存在已经训练好的数据, 开始训练")
        texts = []
        with open(file, 'r') as f:
            for line in f:
                texts.append(json.loads(line)['content'])

        stats = {}
        for i in range(len(texts)):
            print(f"==> 正在训练第{i+1}/{len(texts)}段文本")
            stats = train_input_method(texts[i], stats)
        for i in stats:  # 对记录下的跟随字按字频排序, 取前五十个
            char_freq = stats[i].items()
            stats[i] = [char for char, _ in sorted(char_freq, key=lambda x: x[1], reverse=True)][:50]
        
        with open('out.pickle', 'wb') as f:
            pickle.dump(stats, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"==> 联想输入法数据已训练完成并存入{database}")

    print(f"==> 从{database}中读入联想输入法数据", end='')
    with open(database, 'rb') as f:  # 从数据库中读取跟随字的统计数据
        stats = pickle.load(f, encoding='utf-8')
    while True:
        print("\n==> 请输入 (输入esc退出) :")
        query = input()
        if 'esc' in query:
            break
        input_method(query=query, stats=stats, n=args.number)


if __name__=="__main__":
    main(file='new2016zh/news2016zh_train.json')
