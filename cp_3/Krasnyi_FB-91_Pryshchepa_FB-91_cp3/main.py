import math
import operations as o

path1 = "D:\\Desktop\\учёба\\крипта\\fb-labs-2021\\tasks\\crypto_cp_3\\for_test.utf8\\V9"
path2 = "D:\\Desktop\\учёба\\крипта\\fb-labs-2021\\tasks\\crypto_cp_3\\variants.utf8\\09.txt"
alphabet_ = "абвгдежзийклмнопрстуфхцчшщыьэюя"
alphabet = {alphabet_[x]: x for x in range(31)}  # 'a': 0, 'б': 1...
general_top_bigrams = ["ст", "но", "то", "на", "ен"]


def filter_text(filename):
    file = open(filename, 'r', encoding='utf-8')
    text = file.read().lower()
    file.close()
    if text.find('\n'):
        text = text.replace('\n', '')
    return text


def top_bigrams(text):
    length = len(text)
    if length % 2:
        text = text[0:-1]
        length -= 1
    bigrams_count = {}
    bigrams_frequency = {}
    sorted_bigrams = {}
    for i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
        for j in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            bigrams_count[i + j] = 0
    for i in range(0, length - 1, 2):
        bigram = text[i:i + 2]
        bigrams_count[bigram] += 1
    for key in bigrams_count.keys():
        bigrams_frequency[key] = bigrams_count[key] / (length / 2)
    sorted_values = sorted(bigrams_frequency.values())
    counter = 5
    for i in reversed(sorted_values):
        for k in bigrams_frequency.keys():
            if i == bigrams_frequency[k]:
                sorted_bigrams[k] = i
                counter -= 1
                if counter < 1:
                    return sorted_bigrams


def bigram_pairs(text):
    cipher_top_bigrams = list(top_bigrams(text).keys())
    cipher_pairs = []
    general_pairs = []
    combo_pairs = []
    for i in range(5):
        for j in range(i + 1, 5):
            cipher_pairs.append([cipher_top_bigrams[i], cipher_top_bigrams[j]])
            general_pairs.append([general_top_bigrams[i], general_top_bigrams[j]])
    for pair1 in general_pairs:
        for pair2 in cipher_pairs:
            combo_pairs.append([pair1, pair2])
    return combo_pairs


def find_keys(text):
    pairs = bigram_pairs(text)
    candidates = []
    for pair in pairs:
        x1 = pair[0][0]
        x2 = pair[0][1]
        X1 = alphabet[x1[0]] * 31 + alphabet[x1[1]]
        X2 = alphabet[x2[0]] * 31 + alphabet[x2[1]]
        y1 = pair[1][0]
        y2 = pair[1][1]
        Y1 = alphabet[y1[0]] * 31 + alphabet[y1[1]]
        Y2 = alphabet[y2[0]] * 31 + alphabet[y2[1]]
        # print(f"{y1}: {alphabet[y1[0]]} * 31 + {alphabet[y1[1]]}  = {Y1} ")
        a = o.module_equation(X1 - X2, Y1 - Y2, 31 * 31)
        if a == -1:
            # print("key (a,b) doesn't exist")
            continue
        if type(a) == int:
            b = (Y1 - a * X1) % 31 ** 2
            candidates.append([a, b])
        else:
            for res in a:
                b = (Y1 - res * X1) % 31 ** 2
                candidates.append([res, b])
    return candidates


def decrypter(cipher):
    candidates = find_keys(cipher)
    possible_texts = []
    decrypted_txt = ""
    for pair in candidates:
        for i in range(0, len(cipher), 2):
            a_reversed = o.obernenyi(pair[0], 31 ** 2)
            if a_reversed == -1:
                continue
            y_ = alphabet[cipher[i]] * 31 + alphabet[cipher[i+1]]
            x_ = (a_reversed * (y_ - pair[1])) % 31 ** 2
            x1 = x_ // 31
            x2 = x_ % 31
            decrypted_txt += alphabet_[x1] + alphabet_[x2]
        possible_texts.append(decrypted_txt)
        decrypted_txt = ""
    return possible_texts


def count_frequency(text):
    length = len(text)
    frequency = [text.count(i) / length for i in alphabet_]
    return frequency


def entropy(text):
    frequency_arr = count_frequency(text)
    h = 0
    for p in frequency_arr:
        if p > 0:
            h += p * math.log(p, 2)
    return round(-h, 5)


def recognizer(possible_texts):
    possible_answers = []
    answer = ""
    for variant in possible_texts:
        possible_answers.append([variant[:50], entropy(variant)])
        if entropy(variant) < 4.5:
            answer = f"Answer is found! {variant[:50]}"
    print(answer)
    return possible_answers


text_ = filter_text(path2)
# print(text_)
# bo5_cipher = top_bigrams(text_)
# [print(f"{key}:\t{bo5_cipher[key]}") for key in bo5_cipher]
# keys = find_keys(text_)
# [print(f"({key[0]}, {key[1]})", end='\t') for key in keys]
# txt = decrypter(text_)[0].replace('ь', '_')
# txt = txt.replace('ы', 'ь')
# txt = txt.replace('_', 'ы')
# print(txt)
entropies = recognizer(decrypter(text_))
[print(f"Entropy: {i[1]}\tfor text: {i[0]}") for i in entropies]

