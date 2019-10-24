import sys, re
import xml.etree.ElementTree as et
from nltk.metrics.distance import jaccard_distance
import nltk
from nltk.metrics.scores import accuracy

stopWords = ('a', 'o', 'teu', 'e', 'que', 'tu', 'entao', 'de', 'para', 'me')


def load_KB(input_name):
    perguntas={}
    root = et.parse(input_name).getroot()
    for type_tag in root.findall('documento/faq_list/faq'):
        res_id = type_tag.find('resposta').attrib['id']

        for pergunta in type_tag.findall('perguntas/pergunta'):
            perguntas[res_id] = perguntas.get(res_id, []) + [pergunta.text]
    return perguntas

def load_test_file(test_name):
    perguntas_test =[]
    with open(test_name, 'r', encoding='utf-8') as test_file:
        for line in test_file:
            perguntas_test.append(line)
    return perguntas_test


def main():
    if len(sys.argv) != 3:
        raise ValueError("Usage: <Knowledge Base File> <Test File>")

    input_name = sys.argv[1]
    test_name = sys.argv[2]

    perguntas = load_KB(input_name)
    perguntas_test = load_test_file(test_name)


    perguntas = mapDict(perguntas, preProc)
    perguntas = mapDict(perguntas, removeStopWords)
    perguntas = mapDict(perguntas, tokStem)


    perguntas_test = preProc(perguntas_test)
    perguntas_test = removeStopWords(perguntas_test)
    perguntas_test = tokStem(perguntas_test)

    solution = fileToList("../test/testSolutions2.txt")
    best_acc = 0
    best_threshold = None
    for threshold in range(5,100,5):
        threshold = threshold/100
        j = 0
        results = open("../out/resultados" + str(round(threshold*100)) + ".txt", "w+", encoding='utf-8')
        while j < len(perguntas_test):
            best = 1000
            best_id = None
            pergunta_test = perguntas_test[j]
            for id, listaPerguntas in perguntas.items():
                for pergunta in listaPerguntas:
                    result = jaccard_distance(set(pergunta_test.split()), set(pergunta.split()))
                    if result < best:
                        best_id = id
                        best = result
            if best < threshold:
                results.write(best_id+"\n")
            else:
                results.write("0\n")
            j += 1
        results.close()
        results = fileToList("../out/resultados" + str(round(threshold*100))     + ".txt")

        acc = accuracy(results, solution)
        if acc > best_acc:
            best_acc = acc
            best_threshold = threshold
        print("Accuracy: " + str(acc) + " for " + str(threshold) + " threshold.")
    print("Best Accuracy: " + str(best_acc) + " for " + str(best_threshold) + " threshold.")


def fileToList(fileName):
    res = []
    test_file = open(fileName, 'r', encoding='utf-8')
    for line in test_file:
        res.append(line.strip())
    test_file.close()
    return res


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
        # elimina -
        # l = re.sub(u"-", " ", l)
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
        if len(sentence) == 0:
            continue
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


if __name__ == "__main__":
    main()
