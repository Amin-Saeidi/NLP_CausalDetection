import codecs

from hazm import *


class Loader:
    path_data = '../../data/all.samples.out.txt'
    convert_tags = {'O': 0, 'B-علت': 1, 'I-علت': 2, 'B-معلول': 3, 'I-معلول': 4, 'B-نشانه': 5, 'I-نشانه': 6}

    def __init__(self):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()

    def create_data_label(self):
        lines = codecs.open(self.path_data, 'r', 'utf-8').readlines()

        dataset = {'tokens': [], 'tags': []}
        token_list = []
        label_list = []
        line_number = 1
        error = 0
        for l in lines:
            line_number += 1
            if l in ['\n']:
                if len(token_list) > 0:
                    dataset["tokens"].append(token_list)
                    dataset["tags"].append(label_list)
                    token_list = []
                    label_list = []
                continue

            l = l[0:len(l) - 1]
            w = l.split('\t')
            if len(w) != 2:
                error += 1
                continue

            word = w[0]
            label = w[1]
            word = self.normalizer.normalize(word)
            word = self.lemmatizer.lemmatize(word)
            token_list.append(word)
            try:
                label_list.append(self.convert_tags[label])
            except:
                label_list.append(self.convert_tags['O'])
                print(f"An exception occurred for label = {label} in line_number = {line_number}")

        print(f"Error = {error}")
        return dataset


loader = Loader()
dataset = loader.create_data_label()
