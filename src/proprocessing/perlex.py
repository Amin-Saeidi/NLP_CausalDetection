import codecs

lines = codecs.open('../../data/PERLEX/data.txt', 'r', 'utf-8').readlines()
text_file = codecs.open('../../data/PERLEX/perlex.out.txt', 'w', 'utf-8')
for i in range(len(lines)):
    if i + 1 == len(lines):
        break

    l = lines[i + 1]
    if l != 'Cause-Effect(e2,e1)\n':
        continue
    w_list = lines[i].split('\t')
    text = w_list[1]
    text = text[1:len(text) - 2]
    text = text.replace('<e1>', ' <c> ')
    text = text.replace('</e1>', ' </c> ')
    text = text.replace('<e2>', ' <e> ')
    text = text.replace('</e2>', ' </e> ')
    text_file.writelines(text + ' \n')

text_file.close()
