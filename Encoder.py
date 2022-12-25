from PIL import Image
import numpy as np
import math


codes = []


def run_encoder(width: str, height: str, count: str, path: str):
    global codes

    V_width = int(width)
    V_height = int(height)

    image_partitions = []

    dictionary = dict()

    code_book = []

    temp_vectors = []
    number_of_vectors = int(count)
    image_to_compress = Image.open(path)
    image_to_compress = image_to_compress.convert(mode='L')
    img_array = np.array(image_to_compress)

    create_vectors(number_of_vectors, V_width, V_height, temp_vectors)
    partitioning(img_array, V_width, V_height, image_partitions)
    dictionary[0] = image_partitions
    temp_vectors[0] = calc_average(dictionary[0], V_width, V_height)
    temp_vectors[1] = prev_vector(temp_vectors[0])
    temp_vectors[2] = next_vector(temp_vectors[0])
    classify_vectors(temp_vectors[1], temp_vectors[2], dictionary[0], 1, 2, dictionary)
    encode(V_width, V_height, temp_vectors, dictionary)

    for i in range(len(temp_vectors) - number_of_vectors, len(temp_vectors)):
        code_book.append(temp_vectors[i])

    codes = code_book.copy()
    compress(V_width, V_height, img_array, codes)
    image = Image.fromarray(img_array)
    image.save('compressed.png')


def create_vectors(count: int, width: int, height: int, arr: list):
    for j in range(2 * count - 1):
        arr.append(np.zeros((width, height)))


def partitioning(arr, width: int, height: int, arr_list: list):
    for k in range(0, len(arr), height):
        for b in range(0, len(arr[0]), width):
            temp = arr[k:k + height, b:b + width]
            arr_list.append(temp)


def calc_average(arr: list, width: int, height: int):
    empty = np.zeros((width, height))
    for m in range(0, len(arr)):
        empty += arr[m]
    return empty * round((1 / len(arr)), 10)


def next_vector(arr):
    ans = np.array(arr)
    for n in range(ans.shape[0]):
        for o in range(ans.shape[1]):
            if ans[n][o] != int(ans[n][o]):
                ans[n][o] = math.ceil(ans[n][o])
            else:
                ans[n][o] += 1
    return ans


def prev_vector(arr):
    ans = np.array(arr)
    for p in range(ans.shape[0]):
        for q in range(ans.shape[1]):
            if ans[p][q] != int(ans[p][q]):
                ans[p][q] = math.floor(ans[p][q])
            else:
                ans[p][q] -= 1
    return ans


def classify_vectors(vector1, vector2, arr: list, v1_idx: int, v2_idx: int, dic: dict):
    for vec in arr:
        dis1 = sum(abs((vec - vector1).reshape(-1)))
        dis2 = sum(abs((vec - vector2).reshape(-1)))
        if dis1 > dis2:
            if v2_idx not in dic:
                dic[v2_idx] = list()
            dic[v2_idx].append(vec)
        else:
            if v1_idx not in dic:
                dic[v1_idx] = list()
            dic[v1_idx].append(vec)


def encode(width: int, height: int, arr: list, dic: dict):
    for r in range(1, len(arr)):
        arr[r] = calc_average(dic[r], width, height)
        if 2 * r + 1 < len(arr):
            arr[2 * r + 1] = prev_vector(arr[r])
        if 2 * r + 2 < len(arr):
            arr[2 * r + 2] = next_vector(arr[r])
        if 2 * r + 1 < len(arr) and 2 * r + 2 < len(arr):
            classify_vectors(arr[2 * r + 1], arr[2 * r + 2], dic[r], 2 * r + 1, 2 * r + 2, dic)


def get_nearest(vector, arr):
    x: int = 300
    ret = arr[0]
    test = np.array(vector)
    for vec in arr:
        t = sum((abs(vector - vec)).reshape(-1))
        if t < x:
            x = t
            ret = vec

    return ret


def get_codes():
    return codes


def compress(width: int, height: int, arr, code_blocks: list):
    for s in range(0, len(arr), height):
        for t in range(0, len(arr[0]), width):
            tt = arr[s:s + height, t:t + width]
            c = get_nearest(tt, code_blocks)
            for k in range(len(code_blocks)):
                if (code_blocks[k] == c).all():
                    arr[s:s + height, t:t + width] = k


def decode(width: int, height: int, arr, code_blocks: list):
    for v in range(0, len(arr), height):
        for w in range(0, len(arr[0]), width):
            t = arr[v:v + height, w:w + width]
            c = code_blocks[t[0][0]]
            arr[v:v + height, w:w + width] = c

    image = Image.fromarray(arr)
    image.save('decompressed.png')
