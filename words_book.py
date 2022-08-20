import argparse
from pprint import pprint
import numpy as np
import preprocess 
import random
from collections import OrderedDict
import add_delete_words


def load_dict():
    dict = np.load(preprocess.store_path, allow_pickle = True)["dict"].item()
    print("Load {} words successfully".format(len(dict)))
    return dict

def argument(length: int)-> dict:
    parser = argparse.ArgumentParser(description = "a words book to help you review words")
    parser.add_argument("-t", "--translate", action = "store_true", help = "whether to translate words")
    
    parser.add_argument("-a", "--add", help = "add words to words book", nargs = "+")
    parser.add_argument("-d", "--delete", help = "delete words from words book", nargs = "+")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--size", type = int, help = "specify the size of the book")
    group.add_argument("-r", "--range", type = int, help = "specify the range of the book", nargs = 2)

    args = parser.parse_args()
    args = vars(args)


    if args["size"] is None and args["range"] is None:
        args["size"] = length

    if args["size"] is not None and (args["size"] > length or args["size"] < 0):
        print("Error: size {} is unreasonable".format(args["size"]))
        exit()
    if args["range"] is not None and (args["range"][0] > args["range"][1] or args["range"][0] < 1 or args["range"][1] > length):
        print("Error: range {} is unreasonable".format(args["range"]))
        exit()
    print("args: ", args)
    return args

def words_choose(dict: OrderedDict, args: dict) -> list:
    if args["size"] is not None:
        words = random.sample(list(dict), args["size"])  # 随机选择size个单词
    elif args["range"] is not None:
        words = list(dict)[args["range"][0] - 1 : args["range"][1]]
        random.shuffle(words) # 打乱顺序
    return words

def words_print(dict: OrderedDict, words: list, translate: bool):
    print("\nwords book({} words): \n".format(len(words)))
    for idx, word in enumerate(words):
        if translate:
            print("{} {} : {}".format(idx + 1, word, dict[word]))
        else:
            print("{} {}".format(idx + 1, word))
        print()    
        
    
def main():
    dict = load_dict()
    args = argument(len(dict))

    if args["add"] is not None or args["delete"] is not None:
        print("There are addition and deletion of words. Repreprocessing and no display the words book")
        add_delete_words.main(args["add"], args["delete"])
        preprocess.main()
    else:
        print("No addition or deletion of words. Display the words book")
        words = words_choose(dict, args)
        words_print(dict, words, args["translate"])
    
    
if __name__ == '__main__':
    main()