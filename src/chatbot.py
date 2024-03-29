import sys, re
import xml.etree.ElementTree as et
from nltk.metrics.distance import jaccard_distance
from nltk.metrics.distance import masi_distance
from nltk.metrics.distance import edit_distance
import nltk
from nltk.metrics.scores import accuracy
import numpy as np

import textdistance as td

def main():
    if len(sys.argv) != 3:
        raise ValueError("Usage: <Knowledge Base File> <Test File>")

    perguntas = load_KB(sys.argv[1])
    perguntas_test = load_test_file(sys.argv[2])

    #Pre-process questions
    perguntas = mapDict(perguntas, preProc)
    perguntas = mapDict(perguntas, removeStopWords)
    perguntas = mapDict(perguntas, tokStem)

    #Pre-process test questions
    perguntas_test = preProc(perguntas_test)
    perguntas_test = removeStopWords(perguntas_test)
    perguntas_test = tokStem(perguntas_test)

    #Distances: jaccard, masi, med, dice
    distance = "dice"

    #Read true labels
    solution = fileToList("../test/testSolutions.txt")

    best_acc = 0
    best_threshold = None
    for threshold in setThresholdRange(distance):
        j = 0
        results = open("../out/resultados" + str(threshold) + ".txt", "w+", encoding='utf-8')
        while j < len(perguntas_test):
            best = np.Inf
            best_id = None
            pergunta_test = perguntas_test[j]
            for id, listaPerguntas in perguntas.items():
                for pergunta in listaPerguntas:
                    result = getDistance(distance, pergunta_test, pergunta)
                    if id == "14" and j ==37:
                        a = 0
                    if result < best:
                        best_id = id
                        best = result
                        best_pergunta = pergunta #For debug
            if best < threshold:
                results.write(best_id+"\n")
            else:
                results.write("0\n")
            # if j == 2: #DEBUG
            #     print()
            j += 1
        results.close()
        results = fileToList("../out/resultados" + str(threshold) + ".txt")

        acc = accuracy(results, solution)
        if acc > best_acc:
            best_acc = acc
            best_threshold = threshold
        print("Accuracy: " + str(acc) + " for " + str(threshold) + " threshold.")
    print("Best Accuracy: " + str(best_acc) + " for " + str(best_threshold) + " threshold.")


def load_KB(filename):
    perguntas = {}
    root = et.parse(filename).getroot()
    for type_tag in root.findall('documento/faq_list/faq'):
        res_id = type_tag.find('resposta').attrib['id']

        for pergunta in type_tag.findall('perguntas/pergunta'):
            perguntas[res_id] = perguntas.get(res_id, []) + [pergunta.text]
    return perguntas


def load_test_file(filename):
    perguntas_test = []

    test_file = open(filename, 'r', encoding='utf-8')
    for line in test_file:
        perguntas_test.append(line)
    test_file.close()
    return perguntas_test


def getDistance(distance, str1, str2):
    if distance == "jaccard":
        return jaccard_distance(set(str1.split()), set(str2.split()))
    if distance == "masi":
        return masi_distance(set(str1.split()), set(str2.split()))
    if distance == "med":
        return edit_distance(str1, str2)
    if distance == "dice":
        return 1 - td.sorensen_dice(set(str1.split()), set(str2.split()))
    if distance == "med-set":
        return edit_distance(str1.split(), str2.split())
    else:
        raise ValueError("distance not defined")

def setThresholdRange(distance):
    if distance == "jaccard":
        return np.arange(0.6, 0.9, 0.05)
    if distance == "masi":
        return np.arange(0.75, 0.96, 0.05)
    if distance == "med":
        return np.arange(8, 9, 1)
    if distance == "dice":
        return np.arange(0.5, 0.7, 0.05)
        #return np.arange(0.25, 0.8, 0.05)
    if distance == "med-set":
        return np.arange(0.65, 0.9, 0.05)
    else:
        raise ValueError("distance not defined")

def fileToList(fileName):
    res = []
    test_file = open(fileName, 'r', encoding='utf-8')
    for line in test_file:
        res.append(line.strip())
    test_file.close()
    return res


def mapDict(dic, fun):
    return dict(map(lambda kv: (kv[0], fun(kv[1])), dic.items()))


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
        l = re.sub(u"/", " ", l)
        # TUDO EM MINÚSCULAS
        l = l.lower()
        # ELIMINA PONTUAÇÃO
        l = re.sub("[?|\.|!|:|,|;]", '', l)

        # fica so com as perguntas
        # l = re.sub("^\w+\t+[^\w]", '', l)
        result.append(str(l))
    return result


#stopWords = ('a', 'o', 'teu', 'e', 'que', 'tu', 'entao', 'de', 'para', 'me')
#stopWords = ('a', 'o', 'teu', 'e', 'tu', 'entao', 'para', 'me', 'em', 'que', 'na', 'no', 'nas','ser', 'noutros','sera','uma', 'nestes','neste', 'devo', 'ao')
stopWords = preProc(nltk.corpus.stopwords.words('portuguese'))

def removeStopWords(sentence_list, stopword_list=stopWords):
    perguntas = []

    for sentence in sentence_list:
        sentence = sentence.split()
        if len(sentence) == 0:
            continue
        frase = []
        for word in sentence:
            if word.lower() not in stopword_list:
                frase.append(word)
            fraseAux = ' '.join(frase)
        perguntas.append(fraseAux)
    return perguntas



if __name__ == "__main__":
    main()
