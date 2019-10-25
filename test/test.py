import xml.etree.ElementTree as et
import re
import random
root = et.parse('../res/KB.xml').getroot()

f = open("test3.txt","w+", encoding='utf-8')
f2 = open("testSolutions3.txt","w+", encoding='utf-8')
i = 1
for type_tag in root.findall('documento/faq_list/faq/perguntas'):
    perguntas = type_tag.findall('pergunta')
    index = random.randint(0,len(perguntas)-1)
    pergunta = perguntas[index]
    temp = pergunta.text
    temp = re.sub("[ ]*\n[ ]*", ' ', temp)
    re.sub(u"\n", ' ', pergunta.text)
    f.write( temp + "\n")
    f2.write(str(i) + "\n")
    i+=1
    type_tag.remove(pergunta)


f.close()
f2.close()
tree = et.ElementTree(root)
tree.write("KBTest3.xml", encoding='utf-8')