# 先将collection.txt中的单词及其翻译存入到books.npz中，以便之后的处理

from logging import exception
import numpy as np
from pathlib import Path
from translate import Translator  # 翻译效果较差
from collections import OrderedDict
import tqdm
import pprint
import urllib.request
import urllib.parse
import json

read_path = Path.cwd() / "collection.txt"
store_path = Path.cwd() / "books.npz"

#有道翻译查询入口
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=http://fanyi.youdao.com/'
data = {  #表单数据
    'i': '',
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_CLICKBUTTION',
    'typoResult': 'false'
}

# 以下记录三种翻译方法

# Translator, 超过一定次数后要过一天才能再使用，效果最差
translator = Translator(to_lang = 'zh-CN')

# 有道翻译因为一小时超过1000次被封禁了，在此备份，效果一般
def youdao(word : str) -> str:
    global data
    data['i'] = word

    #对POST数据进行编码
    data_new = urllib.parse.urlencode(data).encode('utf-8')
    #发出POST请求并获取HTTP响应
    response = urllib.request.urlopen(url, data_new)
    #获取网页内容，并进行解码解码
    html = response.read().decode('utf-8')
    #json解析
    target = json.loads(html)
    return target['translateResult'][0][0]['tgt']

# 百度翻译是最好的！最好也不要翻译太多次
def baidu(word):
    base_url = 'https://fanyi.baidu.com/sug'
    # 构建请求对象
    data = {'kw': word}
    data = urllib.parse.urlencode(data)
    # 模拟浏览器
    header = {"User-Agent": "mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    req = urllib.request.Request(url=base_url,data=bytes(data,encoding='utf-8'),headers=header)
    res = urllib.request.urlopen(req)
    # 获取响应的json字符串
    str_json = res.read().decode('utf-8')
    # 把json转换成字典
    myjson = json.loads(str_json)
    return myjson['data'][0]['v']


def loads():
    words = []
    repetition = 0
    with open(read_path, "r") as f:
        for line in f:
            if line != "\n":
                match = line.split(",")
                match = [i.strip() for i in match]
                for word in match:
                    if word in words:
                        repetition += 1
                    else:
                        words.append(word)
    print("Loaded {} words successfully, {} repetition".format(len(words), repetition))
    return words


def trans(words: list) -> OrderedDict: 
    # 如果翻译结果全是英文，认为不成功（偶尔出现）
    def trans_success(result: str)-> bool:
        flag = 0
        alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in result:
            if i not in alpha:
                flag = 1
        if flag == 1:
            return True
        else:
            return False

    dict = OrderedDict()
    error_count = 0
    for word in tqdm.tqdm(words):
        # 按先百度再有道再Translator的顺序翻译
        try:
            result = baidu(word) # 随机报错list out of range
            if trans_success(result) == False:
                raise Exception("trans failure")
        except Exception as e1:
            try:
                print("baidu error, ", e1)
                result = youdao(word) # 报错Expecting value: line 1 column 1 (char 0)，说明被封禁
                if trans_success(result) == False:
                    raise Exception("trans failure")
            except Exception as e2:
                try:
                    print("youdao error, ", e2)
                    result = translator.translate(word)
                    if trans_success(result) == False:
                        raise Exception("trans failure")
                except Exception as e3:
                    print("Translator error, ", e3)
                    result = "error"
                    error_count += 1
        dict[word] = result
    print("Translate {} words successfully, {} error".format(len(dict) - error_count, error_count))
    return dict

def main():
    print("Preprocessing...")
    words = loads()
    dict = trans(words)
    pprint.pprint(dict)
    np.savez(store_path, dict = dict)
    print("Save successfully")


if __name__ == "__main__":
    main()