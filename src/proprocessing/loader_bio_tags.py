import codecs

from hazm import *

class Loader:
    path_data = './sample.out.txt'
    start_tag_list = ['<c>', '<e>']
    end_tag_list = ['</c>', '</e>']
    tag_to_id = {'O': 0, 'B-CAUSE': 1, 'I-CAUSE': 2, 'B-EFFECT': 3, 'I-EFFECT': 4}
    none_tag = 'O'

    def __init__(self):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()

    def create_data_label(self):
        lines = codecs.open(self.path_data, 'r', 'utf-8').readlines()

        dataset = {'tokens': [], 'tags': []}
        data = []
        for sent in lines:
            sent = self.normalizer.normalize(sent)
            token_list = []
            label_list = []
            last_tag = 'O'
            for token in word_tokenize(sent):
                if token in ['<m>', '</m>']:
                    continue
                if token in self.start_tag_list:
                    last_tag = 'B-CAUSE' if token == '<c>' else 'B-EFFECT'
                    continue
                if token in self.end_tag_list:
                    last_tag = 'O'
                    continue

                token_list.append(self.lemmatizer.lemmatize(token))
                label_list.append(self.tag_to_id[last_tag])
                if last_tag == 'B-CAUSE':
                    last_tag = 'I-CAUSE'
                if last_tag == 'B-EFFECT':
                    last_tag = 'I-EFFECT'

            dataset["tokens"].append(token_list)
            dataset["tags"].append(label_list)
        return dataset


loader = Loader()
dataset = loader.create_data_label()
print(f'DataSet = {dataset}')
