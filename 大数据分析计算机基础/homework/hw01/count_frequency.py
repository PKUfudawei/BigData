#!/usr/bin/env python3
import os
import json
import jieba
import pandas as pd


def isChinese(string):
    """
    判断一段字符串是否全为汉字
    """
    for char in string:
        if not (0x4e00<=ord(char)<0x9fa5):
            return False
    
    return True


def count_frequency(text: str, stats: dict = {'char': {}, 'word': {}}):
    """
    统计一段文本的字频(逐字)和词频(通过jieba分词)
    """
    # 统计单字频次
    for char in text:
        if isChinese(char):
            stats['char'][char] = stats['char'].get(char, 0) + 1

    # 统计词语频次
    words = jieba.lcut(text, cut_all=False)
    for word in words:
        if isChinese(word) and len(word)>1:  # 要求word是二字以上词语且全为汉字
            stats['word'][word] = stats['word'].get(word, 0) + 1
    
    return stats


def process_char_frequency(stats: dict):
    """
    处理字频, 输出覆盖80%总字频的汉字、字频、累计字频到HF_SingleHZ.txt (按字频从高到低排序)
    """
    char_freq = list(stats.items())
    char_freq = sorted(char_freq, key=lambda x: x[1], reverse=True)  # 按freq从大到小排序
    char, freq = zip(*char_freq)
    total_freq = sum(freq)
    result = {"汉字": [], "字频": [], "累计字频": []}
    for i in range(len(freq)):
        result['汉字'].append(char[i])
        result['字频'].append(freq[i])
        sum_freq = sum(freq[:i + 1])
        result['累计字频'].append(sum_freq)
        if sum_freq > 0.8 * total_freq:
            break
    
    df = pd.DataFrame(result)
    df.to_csv('HF_SingleHZ.txt', sep='\t', index=True, header=True, encoding='utf-8')
    return result
        

def process_word_frequency(stats: dict):
    """
    处理词频, 输出前一万字频的词语、词频到HF_SingleHZ.txt (按词频从高到低排序)
    """
    word_freq = list(stats.items())
    word_freq = sorted(word_freq, key=lambda x: x[1], reverse=True)  # 按freq从大到小排序
    word, freq = zip(*word_freq)
    result = {"词条": [], "频次": []}
    for i in range(10000):
        result['词条'].append(word[i])
        result['频次'].append(freq[i])
        if i>=len(word_freq):
            break
    
    df = pd.DataFrame(result)
    df.to_csv('HF_Word.txt', sep='\t', index=True, header=True, encoding='utf-8')
    return result


def main(file: str):
    """
    file代表用于统计频次的文件路径, 统计完成后把数据存入'HF_SingleHZ.txt'和'HF_Word.txt'
    """
    if not (os.path.exists('HF_SingleHZ.txt') and os.path.exists('HF_Word.txt')):
        print("不存在已经统计好的频次数据, 开始统计")
        texts = []
        with open(file, 'r') as f:
            for line in f:
                texts.append(json.loads(line)['content'])

        stats = {'char': {}, 'word': {}}
        for i in range(len(texts)):
            print(f"==> 正在统计第{i+1}/{len(texts)}段文本")
            stats = count_frequency(texts[i], stats)
            
        process_char_frequency(stats=stats['char'])
        process_word_frequency(stats=stats['word'])
    
    print("==> 频次数据已统计并储存, 请查看")


if __name__=="__main__":
    main(file='new2016zh/news2016zh_train.json')
