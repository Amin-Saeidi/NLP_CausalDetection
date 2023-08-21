import codecs

def process_line_format_1(line):
    see_marketer = False
    see_caused = False
    see_effect = False
    result = ''
    r = []
    i = 0
    while i < len(line):
        if line[i] != '*':
            result += line[i]
            i += 1
            continue
        if i + 1 == len(line):
            if not see_caused:
                print('error')
            else:
                result += ' </c> '
                see_caused = False
            i += 1
            continue

        if i + 1 < len(line) and line[i + 1] != '*':
            if not see_caused:
                result += ' <c> '
                see_caused = True
            else:
                result += ' </c> '
                see_caused = False
            i += 1
            continue

        if i + 2 < len(line) and line[i + 1] == '*' and line[i + 2] != '*':
            if not see_marketer:
                result += ' <m> '
                see_marketer = True
            else:
                result += ' </m> '
                see_marketer = False
            i += 2
            continue

        if i + 2 < len(line) and line[i + 1] == '*' and line[i + 2] == '*':
            if not see_effect:
                result += ' <e> '
                see_effect = True
            else:
                result += ' </e> '
                see_effect = False
            i += 3
            continue

    return result


def process_line_format_2(line):
    see_marketer = False
    see_caused = False
    see_effect = False
    result = ''
    r = []
    i = 0
    while i < len(line):
        if line[i] not in ['*', '&', '+']:
            result += line[i]
            i += 1
            continue
        if line[i] == '*':
            if not see_caused:
                result += ' <c> '
                see_caused = True
            else:
                result += ' </c> '
                see_caused = False
            i += 1
            continue
        if line[i] == '&':
            if not see_caused:
                result += ' <m> '
                see_caused = True
            else:
                result += ' </m> '
                see_caused = False
            i += 1
            continue
        if line[i] == '+':
            if not see_caused:
                result += ' <e> '
                see_caused = True
            else:
                result += ' </e> '
                see_caused = False
            i += 1
            continue

    return result

# example
# lines = codecs.open('sample.moslemi.txt', 'r', 'utf-8').readlines()
# text_file = codecs.open('sample.moslemi.out.txt', 'w', 'utf-8')
# for line in lines:
#     text_file.writelines(process_line_format_2(line))
# text_file.close()

lines = codecs.open('sample.akbari.txt', 'r', 'utf-8').readlines()
text_file = codecs.open('sample.akbari.out.txt', 'w', 'utf-8')
for line in lines:
    text_file.writelines(process_line_format_1(line))
text_file.close()
