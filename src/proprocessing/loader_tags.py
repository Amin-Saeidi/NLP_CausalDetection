import codecs

from hazm import *

class Loader:
    path_data = 'sample.out.txt'
    start_tag_list = ['<c>', '<m>', '<e>']
    end_tag_list = ['</c>', '</m>', '</e>']
    none_tag = '<none>'

    def __init__(self):
        self.normalizer = Normalizer()
        self.lemmatizer = Lemmatizer()

    def create_data_label(self):
        lines = codecs.open(self.path_data, 'r', 'utf-8').readlines()

        sent_token_list = []
        sent_label_list = []
        for sent in lines:
            sent = self.normalizer.normalize(sent)
            token_list = []
            label_list = []
            last_tag = self.none_tag
            for token in word_tokenize(sent):
                if token in self.start_tag_list:
                    last_tag = token
                    continue
                if token in self.end_tag_list:
                    last_tag = self.none_tag
                    continue

                token_list.append(self.lemmatizer.lemmatize(token))
                label_list.append(last_tag)

            sent_token_list.append(token_list)
            sent_label_list.append(label_list)
        return sent_token_list, sent_label_list


loader = Loader()
sent_token_list, sent_label_list = loader.create_data_label()
print("sss")
