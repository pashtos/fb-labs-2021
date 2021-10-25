alphabet_ = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
alphabet = {alphabet_[x]: x for x in range(32)}  # 'a': 0, 'б': 1...
keys = [
    'да',
    'нет',
    'пять',
    'ответ',
    'десятьбукв',
    'авиатопливо',
    'безбарьерный',
    'геофизический',
    'нагревательный',
    'взбунтовавшийся',
    'делопроизводство',
    'европарламентарий',
    'североамериканский',
    'товаропроизводитель',
    'иммуностимулирование'
]

source_file = open('open_text.txt', 'r', encoding='utf-8')
source_text = source_file.read()
source_file.close()

encrypted_file = open('encrypted_text.txt', 'r', encoding='utf-8')
encrypted_text = (encrypted_file.read()).replace("\n", '')
encrypted_file.close()
encrypted_file = open('encrypted_text.txt', 'w', encoding='utf-8')
encrypted_file.write(encrypted_text)
encrypted_file.close()


def encrypt(text: str, key: str):
    keylen = len(key)
    encrypted_text = ''
    for i in range(len(text)):
        encrypted_text += alphabet_[(alphabet[text[i]] + alphabet[key[i % keylen]]) % 32]
    return encrypted_text


def affinity_index(txt: str):
    frequency = {x: txt.count(x) for x in alphabet_}
    a_index = 0
    for x in frequency.keys():
        a_index += frequency[x] * (frequency[x] - 1)
    n = len(txt)
    a_index *= 1 / (n ** 2 - n)
    return a_index


def create_blocks(text: str, r: int):
    blocks = []
    for j in range(0, r):
        sub_block = ""
        for l in range(0, len(text) - j, r):
            sub_block += text[l + j]
        if len(sub_block):
            blocks.append(sub_block)
        else:
            continue
    return blocks


def find_key_length(text: str):
    blocks = {}
    for r in range(2, 31):
        blocks[r] = create_blocks(text, r)
    affinity_indexes = {}
    for i in blocks.keys():
        avg_index = 0
        for j in blocks[i]:
            avg_index += affinity_index(j)
        avg_index /= len(blocks[i])
        affinity_indexes[i] = avg_index
        print(f"keylen: {i}\tI = {affinity_indexes[i]}")
    max_val = max(affinity_indexes.values())
    for k in affinity_indexes.keys():
        if affinity_indexes[k] == max_val:
            return k


def guess_key(r: int, cipher: str):
    general_top_letters = 'оеаи'
    key = ""
    blocks = create_blocks(cipher, r)
    for general_letter in general_top_letters:
        for block in blocks:
            max_frequency = 0
            max_letter = ''
            for letter in alphabet_:
                if block.count(letter) > max_frequency:
                    max_frequency = block.count(letter)
                    max_letter = letter
            key += alphabet_[(alphabet[max_letter] - alphabet[general_letter] + 32) % 32]
        print(f"letter:{general_letter}\tkey: {key}")
        key = ""
    return key


def decrypt(cipher: str, key: str):
    keylen = len(key)
    decrypted_text = ''
    for i in range(len(cipher)):
        decrypted_text += alphabet_[(alphabet[cipher[i]] - alphabet[key[i % keylen]] + 32) % 32]
    return decrypted_text


# print(f"I для відкритого тексту(нашого):{affinity_index(source_text)}")
# print('\n')
# for i in keys:
#     print(f"I для шифрованого, ключ {i}: {affinity_index(encrypt(source_text, i))}")
# print('\n')
# print("I при підборі ключів для шифрованого тексту, r = 1,2...30")
# find_key_length(encrypted_text)
# freq_file = open('letters_frequency.txt', 'w', encoding='utf-8')
# result = ""
# length = len(encrypted_text)
# for letter in alphabet_:
#     result += letter + '\t' + str(encrypted_text.count(letter)/length) + '\n'
# freq_file.write(result)
# freq_file.close()