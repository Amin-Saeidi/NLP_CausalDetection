import codecs

from hazm import *

class ConvertStandardFormat:
    path_data = '../../data/samples.out.txt'
    start_tag_list = ['<c>', '<e>', '<m>']
    end_tag_list = ['</c>', '</e>', '</m>']
    none_tag = 'O'

    def convert(self):
        lines = codecs.open(self.path_data, 'r', 'utf-8').readlines()
        text_file = codecs.open('../../data/samples.standard.out.txt', 'w', 'utf-8')

        for sent in lines:
            last_tag = 'O'
            for token in word_tokenize(sent):
                if token in ['\r', '\n']:
                    continue

                if token in self.start_tag_list:
                    if token == '<c>':
                        last_tag = 'B-علت'
                    elif token == '<e>':
                        last_tag = 'B-معلول'
                    else:
                        last_tag = 'B-نشانه'
                    continue

                if token in self.end_tag_list:
                    last_tag = 'O'
                    continue

                token = token.replace('\r', '')
                text = token + '\t' + last_tag
                text_file.writelines(text + '\n')
                if last_tag == 'B-علت':
                    last_tag = 'I-علت'
                if last_tag == 'B-معلول':
                    last_tag = 'I-معلول'
                if last_tag == 'B-نشانه':
                    last_tag = 'I-نشانه'

            text_file.writelines('\r\n')

        text_file.close()


loader = ConvertStandardFormat()
loader.convert()
