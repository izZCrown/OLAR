import os
import yaml
import numpy as np
from scipy.spatial.distance import cosine
import spacy
nlp = spacy.load("en_core_web_sm")


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_config_dict_to_opt(opt, config_dict):
    if not isinstance(config_dict, dict):
        raise TypeError("Config must be a Python dictionary")
    for k, v in config_dict.items():
        k_parts = k.split('.')
        pointer = opt
        for k_part in k_parts[:-1]:
            if k_part not in pointer:
                pointer[k_part] = {}
            pointer = pointer[k_part]
            assert isinstance(pointer, dict), "Overriding key needs to be inside a Python dict."
        ori_value = pointer.get(k_parts[-1])
        pointer[k_parts[-1]] = v

def load_opt(conf_file):
    default_path = './tools/OpenSeeD/configs/openseed/openseed_swint_lang.yaml'
    if conf_file is  None:
        conf_file = default_path
    opt = {}
    with open(conf_file, encoding='utf-8') as f:
        config_dict = yaml.safe_load(f)

    load_config_dict_to_opt(opt, config_dict)

    return opt

def uint82bin(n, count=8):
    return ''.join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])


def labelcolormap(N):
    cmap = np.zeros((N, 3), dtype=np.uint8)
    for i in range(N):
        r, g, b = 0, 0, 0
        id = i + 1  # let's give 0 a color
        for j in range(7):
            str_id = uint82bin(id)
            r = r ^ (np.uint8(str_id[-1]) << (7 - j))
            g = g ^ (np.uint8(str_id[-2]) << (7 - j))
            b = b ^ (np.uint8(str_id[-3]) << (7 - j))
            id = id >> 3
        cmap[i, 0] =  r
        cmap[i, 1] =  g
        cmap[i, 2] =  b
     
    return cmap

class Colorize(object):
    def __init__(self, n=182):
        self.cmap = labelcolormap(n)

    def __call__(self, gray_image):
        size = gray_image.shape
        color_image = np.zeros((3, size[0], size[1])) 
     
        for label in range(0, len(self.cmap)):
            mask = (label == gray_image ) 
            color_image[0][mask] = self.cmap[label][0]
            color_image[1][mask] = self.cmap[label][1]
            color_image[2][mask] = self.cmap[label][2]

        return color_image

def category_to_coco(model, category, coco_categories):
    '''Map objects to categories in Coco

    :param model: _description_
    :param category: _description_
    :param coco_categories: _description_
    :return: _description_
    '''
    category_embedding = model.encode([category.lower()])[0]
    distances = []
    for item in coco_categories:
        cos_dis = cosine(category_embedding, item['embed'])
        distances.append(cos_dis)
    for i, item in enumerate(distances):
        print(f'{i}: {item}: {coco_categories[i]["category"]}')
    min_dis = min(distances)
    min_index = distances.index(min_dis)
    category = coco_categories[min_index]['category']
    return category

def pos_tag(sentence):
    '''_summary_

    :param sentence: _description_
    :return: nouns, num_tag: is there a quantifier before a noun
    '''
    nouns = []
    num_tag = {}
    targets = ['NOUN', 'PROPN']
    tokens = nlp(sentence)

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.pos_ in targets:
            noun = token.text
            if i + 1 < len(tokens) and tokens[i+1].pos_ in targets:
                noun += ' ' + tokens[i+1].text
                i += 1
            num_tag[noun] = False

            if i > 0 and tokens[i-1].pos_ == 'NUM':
                count = w2n.word_to_num(tokens[i-1].text)
                nouns.extend([noun] * count)
                num_tag[noun] = True
            else:
                nouns.append(noun)
        i += 1
    return nouns, num_tag

