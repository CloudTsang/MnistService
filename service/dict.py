import json


def get_dict(txt):
    # 获取labels
    label = open(txt, "r", encoding='utf-8')
    content = label.read()
    content = content.strip(" ")
    if content is None or content == '':
        return {}
    return json.loads(content)


def save_dict(content, txt):
    with open(txt, "w", encoding='utf-8') as label:
        label.write(json.dumps(content))


def add_trace(trace, ty):
    if not ty in dict:
        dict[ty] = []
    arr = dict[ty]
    is_added = False
    if arr is not None:
        for i in range(len(arr)):
            if arr[i] == trace:
                is_added = True
                print('Trace has added.')
                break
    if not is_added:
        dict[ty].append(trace)
        # print('dict:', dict)
        save_dict(dict, dict_path)


def check_trace(s):
    for i in dict:
        arr = dict[i]
        for tmp_s in arr:
            if tmp_s in s:
                s = s.replace(tmp_s, i)
    return s

dict_path = "dict.txt"
dict = get_dict(dict_path)
# print("trace data:", dict)

if __name__ == '__main__':
    print(check_trace('443∟13'))
    # dict['2'] = [['2']]
    # save_dict(dict, dict_path)