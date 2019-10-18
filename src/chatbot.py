import sys, re
import xml.etree.ElementTree as et

import nltk

stopWords = ('a', 'o', 'teu', 'e', 'que', 'tu', 'entao', 'de', 'para', 'me')


def main():
    if len(sys.argv) != 3:
        raise ValueError("Usage: <Knowledge Base File> <Test File>")

    input_name = sys.argv[1]
    test_name = sys.argv[2]

    perguntas = {}
    perguntas_test = []

    root = et.parse(input_name).getroot()
    for type_tag in root.findall('documento/faq_list/faq'):
        res_id = type_tag.find('resposta').attrib['id']

        for pergunta in type_tag.findall('perguntas/pergunta'):
            perguntas[res_id] = perguntas.get(res_id, []) + [pergunta.text]

    perguntas = mapDict(perguntas, preProc)
    perguntas = mapDict(perguntas, removeStopWords)
    perguntas = mapDict(perguntas, tokStem)

    test_file = open(test_name, 'r', encoding='utf-8')
    for line in test_file:
        perguntas_test.append(line)
    test_file.close()

    perguntas_test = preProc(perguntas_test)
    perguntas_test = removeStopWords(perguntas_test)
    perguntas_test = tokStem(perguntas_test)


def mapDict(dic, fun):
    return dict(map(lambda kv: (kv[0], fun(kv[1])), dic.items()))


def preProc(Lista):
    result = []
    for l in Lista:
        # ELIMINA ACENTOS
        l = re.sub(u"ã", 'a', l)
        l = re.sub(u"á", "a", l)
        l = re.sub(u"à", "a", l)
        l = re.sub(u"õ", "o", l)
        l = re.sub(u"ô", "o", l)
        l = re.sub(u"ó", "o", l)
        l = re.sub(u"é", "e", l)
        l = re.sub(u"ê", "e", l)
        l = re.sub(u"í", "i", l)
        l = re.sub(u"ú", "u", l)
        l = re.sub(u"ç", "c", l)
        l = re.sub(u"Ã", 'A', l)
        l = re.sub(u"Á", "A", l)
        l = re.sub(u"À", "A", l)
        l = re.sub(u"Õ", "O", l)
        l = re.sub(u"Ô", "O", l)
        l = re.sub(u"Ô", "O", l)
        l = re.sub(u"Ó", 'O', l)
        l = re.sub(u"Í", "I", l)
        l = re.sub(u"Ú", "U", l)
        l = re.sub(u"Ç", "C", l)
        l = re.sub(u"É", "E", l)
        l = re.sub(u"-", " ", l)
        # TUDO EM MINÚSCULAS
        l = l.lower()
        # ELIMINA PONTUAÇÃO
        # l = re.sub("[?|\.|!|:|,|;]", '', l)
        # fica so com as perguntas
        # l = re.sub("^\w+\t+[^\w]", '', l)
        result.append(str(l))
    return result


def removeStopWords(sentence_list, stopword_list=stopWords):
    perguntas = []
    for sentence in sentence_list:
        sentence = sentence.split()
        frase = []
        for word in sentence:
            if word.lower() not in stopword_list:
                frase.append(word)
            fraseAux = ' '.join(frase)
        perguntas.append(fraseAux)
    return perguntas


def tokStem(perguntas):
    perguntas_tok_stem = []
    stemmer = nltk.stem.RSLPStemmer()
    for l in perguntas:
        l = nltk.word_tokenize(l)
        l1 = []
        tagged = nltk.pos_tag(l)
        for word in l:
            word = stemmer.stem(word)
            l1.append(word)
        l = ' '.join(l1)
        perguntas_tok_stem.append(l)
    return perguntas_tok_stem


main()
