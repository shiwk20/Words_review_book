from preprocess import read_path
import os


def add(add_words: list): # 一行最多打印10个单词,不查重
    with open(read_path, mode = "a") as f:
        if os.path.getsize(read_path) != 0:
            f.write("\r\n")
        for i in range(len(add_words) // 10 + 1):
            if i == len(add_words) // 10:
                tmp = add_words[10 * i:]
                f.write(", ".join(tmp))
            else:
                tmp = add_words[10 * i: 10 * (i + 1)]
                f.write(", ".join(tmp))
                f.write("\r\n")
    f.close()
    print("add {} words successfully".format(len(add_words)))

def delete(delete_words: list):
    # 首先读取文件内容
    try:
        with open(read_path, mode = "r") as f:
            if os.path.getsize(read_path) == 0:
                print("empty file, no words to delete")
                return
            else:
                lines = f.readlines()
        f.close()
    except Exception as e:
        print(e)
        return 

    # 删除单词
    idx = 0
    success_count = 0
    while idx < len(lines):
        if lines[idx] != "\n":
            match = lines[idx].split(",")
            match = [i.strip() for i in match]
            flag = 0
            for word in delete_words:
                if word in match:
                    match.remove(word)
                    success_count += 1
                    flag = 1
            if len(match) == 0:
                lines.pop(idx)
                if idx == len(lines):
                    if idx != 0:
                        lines.pop(idx - 1)
                        idx -= 2
                else:    
                    lines.pop(idx)
                    idx -= 1
            elif flag == 1:
                lines[idx] = ", ".join(match) + "\n"
        idx += 1
    lines[-1] = lines[-1].replace("\n", "")

    # 重新写入文件
    with open(read_path, mode = "w") as f:
        f.writelines(lines)
    f.close()

    print("delete {} words successfully, {} error".format(success_count, len(delete_words) - success_count))



def main(add_words, delete_words):
    if add_words is not None:
        add(add_words)
    if delete_words is not None:
        delete(delete_words)



if __name__ == "__main__":
    main()